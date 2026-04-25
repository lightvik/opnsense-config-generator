# План: opnsense-config-generator

Генератор `config.xml` для OPNsense из документированного Jinja2-шаблона `config.yaml.j2`.

---

## 1. Цель и сценарий использования

**Сценарий**: one-shot import. Пользователь редактирует `config.yaml.j2`, генерирует `config.xml`, импортирует его в свежеустановленный OPNsense через GUI (System → Configuration → Backups → Restore). Дальше OPNsense ведёт конфигурацию сам через GUI. Повторная регенерация не предполагается.

Импорт — стартовая точка для новой инсталляции. Не GitOps.

## 2. Технологический стек

- **Python 3.12+**
- **Jinja2** — рендеринг `config.yaml.j2` → `config.yaml`
- **PyYAML** — парсинг рендера
- **pydantic v2** — строгий контракт на YAML (валидация + типы)
- **lxml** — построение и сериализация XML
- **pip + requirements.txt / requirements-dev.txt** — зависимости (без uv/poetry; позже мигрируем в Dockerfile)
- **ruff** — линтер + форматтер
- **mypy** strict + плагин `pydantic.mypy`
- **pytest** — тесты

## 3. Поток данных

```
config.yaml.j2  ──(Jinja2 + env)──▶  config.yaml  ──(pydantic validate)──▶  Model  ──(builders)──▶  config.xml
                                       (артефакт                                                       (итог)
                                        на диске,
                                        для отладки)
```

Промежуточный `config.yaml` сохраняется на диск (по умолчанию рядом с выходом, либо в `--intermediate <path>`).

CLI:
```
opnsense-config-generator render \
    --template config.yaml.j2 \
    --intermediate build/config.yaml \
    --output build/config.xml
```

В шаблоне доступны:
- `env` — словарь с переменными окружения (как в примере `inventory.yaml.j2` — `{{ env.MY_VAR }}`, `{{ env.get('X', 'default') }}`). Сейчас jinja-конструкции не используются, но техническая возможность есть.
- `load_yaml('path.yaml')` — глобал для подгрузки сторонних YAML (на будущее, под secrets).

## 4. Привязка к версии OPNsense

- Целевая версия — **последняя стабильная community-версия OPNsense на момент релиза первой версии** (на 2026-04 это ориентировочно 25.x/26.x — фиксируем точно при первом sync; см. github.com/opnsense/core теги).
- Версия захардкожена в `opnsense_config_generator/version.py` как константа `OPNSENSE_VERSION`.
- В сгенерированный `config.xml` пишется `<version>X.Y</version>` именно этой версии.
- Каталог `opnsense_reference/` хранит дамп файлов из исходников OPNsense нужного тега:
  - `default_config.xml` — `src/etc/config.xml` из репо `opnsense/core`
  - `mvc_models/` — формальные XML-модели плагинов из `src/opnsense/mvc/app/models/OPNsense/<plugin>/<Model>.xml` (Wireguard, Kea, и т.д.)
  - `VERSION` — текстовый файл с версией
  - `README.md` — инструкция по обновлению
- `scripts/sync_opnsense_reference.py` — выкачивает нужные файлы по тегу/ветке через GitHub raw URL и кладёт в `opnsense_reference/`.
- `scripts/check_new_opnsense_release.py` — для опционального CI cron-job: проверяет github releases и открывает issue если есть новый stable-релиз.
- При смене `OPNSENSE_VERSION`: запускаем sync-скрипт → смотрим diff → правим pydantic-модели и builders под изменения → чиним golden-тесты → релиз.

**Важный нюанс**: у OPNsense нет единого XSD. Часть legacy-секций (`system`, `interfaces`, `filter`, `nat`, `dhcpd`, `unbound`, ...) описана только в PHP-исходниках — наши pydantic-модели и builders для них пишутся вручную с эталоном через golden-файлы. Часть новых плагинов (Wireguard, Kea DHCP, Captive Portal, Quagga) имеет формальные XML Model.xml — для них структуру можно частично выводить из этих моделей, но всё равно валидируем своими pydantic-моделями.

## 5. UUID

**Решение**: детерминированный uuid5 от стабильного ключа `"<section>:<name>"` с фиксированным namespace UUID, захардкоженным в `uuid_utils.py`.

```python
NAMESPACE = uuid.UUID("FIXED-UUID-CONST-...")  # сгенерировать один раз при инициализации проекта
def make_uuid(section: str, name: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{section}:{name}"))
```

Преимущества для one-shot сценария: golden-тесты стабильны без маскирования, два рендера одного YAML дают идентичный XML, diff в git осмысленный. Переопределение UUID через YAML не нужно.

## 6. Revision

**Решение**: фиксированный блок при каждом рендере.

```xml
<revision>
  <username>opnsense-config-generator</username>
  <time>{{ timestamp генерации }}</time>
  <description>Imported by opnsense-config-generator vX.Y.Z (OPNsense X.Y)</description>
</revision>
```

Дальше OPNsense сам ведёт историю в `/conf/backup/`.

## 7. Объём поддерживаемых секций

**Цель**: полное покрытие всех секций `config.xml` для целевой версии OPNsense.

**Реализация — поэтапно** (см. Roadmap ниже). Базовый набор секций (минимум для рабочего firewall):

Этап 1 (MVP, минимально работающая инсталляция):
- `system` — hostname, domain, dns servers, timezone, web GUI, SSH, users, groups
- `interfaces` — assignments (LAN/WAN/OPT), IPv4/IPv6 конфиги
- `vlans`, `bridges`, `laggs`
- `gateways` + статические маршруты (`staticroutes`)
- `filter` (правила фаервола) + `aliases`
- `nat` (outbound, port forward, 1:1)
- `dnsmasq` — DNS Forwarder + DHCP (OPNsense 26.x; ISC dhcpd удалён)
- `unbound` (DNS resolver)

Этап 2:
- `openvpn`
- `wireguard` (через MVC plugin)
- `ipsec`
- `cert`, `ca` (PKI)
- `ntpd`, `syslog`

Этап 3 (полнота):
- `monit`, `cron`, `snmpd`
- остальные MVC-плагины (Captive Portal, Quagga, Diagnostics и т.д.)
- любые недостающие legacy-секции

## 8. Пароли пользователей

bcrypt-хэш генерируется самим инструментом из plaintext-пароля в YAML. Используем `bcrypt` библиотеку. Пароль из YAML никогда не попадает в XML — только хэш.

```yaml
users:
  - name: admin
    password: "secret"   # plaintext в YAML
    # → в XML пишется bcrypt-хэш
```

В будущем (когда займёмся secrets) — поддержка `password_hash:` для уже захэшированных или `password_env: VAR_NAME`.

## 9. Структура каталогов

```
config-generator/
├── PLAN.md                              # этот файл
├── README.md                            # quickstart + описание + инструкция
├── config.yaml.j2                       # рабочий шаблон (пользователь редактирует)
├── pyproject.toml                       # ruff/mypy конфиг + проектная мета
├── requirements.txt                     # runtime deps
├── requirements-dev.txt                 # + ruff, mypy, pytest
├── .python-version
├── .gitignore
│
├── opnsense_config_generator/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                           # CLI entrypoint (argparse)
│   ├── version.py                       # OPNSENSE_VERSION, TOOL_VERSION
│   ├── render.py                        # Jinja2: yaml.j2 → yaml
│   ├── build.py                         # пайплайн: yaml → pydantic → xml
│   ├── uuid_utils.py                    # NAMESPACE, make_uuid()
│   ├── revision.py                      # build_revision_block()
│   ├── xml_utils.py                     # lxml хелперы, сериализация с pretty-print
│   ├── password.py                      # bcrypt
│   ├── models/                          # pydantic-схемы YAML-контракта
│   │   ├── __init__.py
│   │   ├── root.py                      # OpnSenseConfig (корень)
│   │   ├── system.py
│   │   ├── interfaces.py
│   │   ├── vlans.py
│   │   ├── bridges.py
│   │   ├── laggs.py
│   │   ├── filter.py
│   │   ├── nat.py
│   │   ├── aliases.py
│   │   ├── dnsmasq.py
│   │   ├── unbound.py
│   │   ├── gateways.py
│   │   ├── routes.py
│   │   ├── openvpn.py          # (Этап 4)
│   │   ├── wireguard.py        # (Этап 4)
│   │   ├── ipsec.py            # (Этап 4)
│   │   ├── ntpd.py             # (Этап 4)
│   │   ├── syslog.py           # (Этап 4)
│   │   ├── certs.py            # (Этап 4)
│   │   └── ...
│   └── builders/                        # YAML-модель → lxml.etree.Element
│       ├── __init__.py
│       ├── base.py                      # базовый Builder, утилиты
│       ├── system.py
│       ├── interfaces.py
│       ├── filter.py
│       └── ... (по одному на секцию)
│
├── docs/
│   ├── minimal_config.yaml.j2           # справочный шаблон: только основные секции
│   └── full_config.yaml.j2              # справочный шаблон: все секции и опции
│
├── opnsense_reference/                  # справочники из upstream OPNsense
│   ├── VERSION                          # 26.1.6
│   ├── default_config.xml
│   ├── mvc_models/
│   │   ├── Wireguard/
│   │   ├── Kea/
│   │   └── ...
│   └── README.md                        # как обновлять
│
├── scripts/
│   ├── sync_opnsense_reference.py
│   └── check_new_opnsense_release.py
│
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── test_models_validation.py    # pydantic-валидация
    │   ├── test_uuid.py
    │   ├── test_revision.py
    │   ├── test_render.py               # Jinja2-рендер
    │   └── test_password.py
    ├── snapshots/                       # snapshot-тесты по секциям (text-файлы под git)
    │   ├── system/
    │   │   ├── basic.yaml
    │   │   └── basic.expected.xml
    │   ├── filter/
    │   └── ...
    ├── golden/                          # golden-тесты на полный config.xml
    │   ├── minimal/
    │   │   ├── config.yaml              # входной YAML для minimal golden-теста
    │   │   └── expected.xml
    │   ├── typical/                     # (Этап 4)
    │   └── full/                        # (Этап 5)
    ├── test_snapshots.py
    ├── test_golden.py
    └── test_xml_wellformed.py
```

## 10. Тестирование

Слои (в CI запускаются все, кроме smoke-теста):

1. **Unit-тесты pydantic-моделей** — валидация (типы, диапазоны, обязательные поля).
2. **Unit-тесты вспомогательных модулей** — `uuid_utils`, `revision`, `password`, `render`.
3. **Snapshot-тесты по секциям** — для каждой секции маленький YAML → XML, сравниваем с зафиксированным `*.expected.xml` под git. Помогает локализовать регрессии.
4. **Golden-тесты на полные конфиги** — `minimal.yaml`, `typical.yaml`, `full.yaml` → ожидаемый `config.xml`. Самые важные интеграционные тесты.
5. **XML well-formedness** — lxml парсит вывод без ошибок, корневой элемент `<opnsense>`, версия совпадает с `OPNSENSE_VERSION`.
6. **Diff против `default_config.xml`** — для пустого ввода наш вывод должен быть совместимым подмножеством дефолта (sanity).

**Smoke-тест на живом OPNsense** — вручную перед каждым релизом или сменой версии OPNsense (загрузка в qemu/Vagrant, импорт сгенерированного XML, проверка что система загружается и интерфейсы поднялись). Не в CI.

Snapshot-обновление — флагом `pytest --update-snapshots` (реализовать вручную, без `syrupy`, чтобы хранить как обычные текстовые файлы в git).

## 11. Линтинг и качество кода

В `pyproject.toml`:
- **ruff** (`ruff check`, `ruff format`) — заменяет black/isort/flake8.
- **mypy** в strict-режиме + `plugins = ["pydantic.mypy"]`.
- **pre-commit** хуки (опционально, не обязателен в первой версии).

CI команды (для будущего CI yaml, когда будет нужно):
```
ruff check .
ruff format --check .
mypy opnsense_config_generator
pytest
```

## 12. Документация

- `README.md` — полное описание проекта: установка, использование, параметры CLI, поддерживаемые секции, секция разработки.
- `config.yaml.j2` (корень) — рабочий шаблон, который пользователь редактирует:
  - минимальная рабочая конфигурация (WAN/LAN, пользователь, DHCP, DNS, правила)
  - краткие inline-комментарии для неочевидных полей
  - указатель на `docs/` для полной документации
- `docs/minimal_config.yaml.j2` — справочный шаблон только основных секций (system, interfaces, filter, nat, dnsmasq, unbound):
  - шапка с описанием Jinja2-возможностей (env, load_yaml, условия, циклы)
  - все опциональные поля закомментированы с примерами и дефолтами
- `docs/full_config.yaml.j2` — справочный шаблон всех секций:
  - то же, что minimal, плюс vlans, bridges, laggs, gateways, staticroutes, aliases
  - расширенные примеры (несколько пользователей, PPPoE, port forwarding, 1:1 NAT, DHCP-резервации, Unbound overrides)
- `opnsense_reference/README.md` — как обновлять reference при новой версии OPNsense.

---

## 13. Roadmap (этапы исполнения)

Статусы: ✅ сделано · 🔲 предстоит

### Этап 0 — каркас проекта ✅

1. ✅ Создать структуру каталогов (см. §9), пустые `__init__.py`.
2. ✅ `pyproject.toml` с метаданными пакета, конфигом ruff и mypy.
3. ✅ `requirements.txt` (jinja2, pyyaml, pydantic>=2, lxml, bcrypt) и `requirements-dev.txt` (+ ruff, mypy, pytest).
4. ✅ `.gitignore`, `.python-version`.
5. ✅ `README.md` — quickstart.
6. ✅ `version.py` — `OPNSENSE_VERSION = "26.1.6"`, `TOOL_VERSION = "0.1.0"`.
7. ✅ Запустить `scripts/sync_opnsense_reference.py` — скачан `default_config.xml` и 23 MVC-модели для тега `26.1.6`.

### Этап 1 — инфраструктура генератора ✅

1. ✅ `opnsense_reference/` — заполнен через sync-скрипт.
2. ✅ `uuid_utils.py` — константный NAMESPACE UUID (DNS), `make_uuid(section, name)`.
3. ✅ `revision.py` — `build_revision_block()`.
4. ✅ `password.py` — bcrypt-хэш из plaintext (`hash_password`).
5. ✅ `xml_utils.py` — обёртка над lxml: 2-пробельный отступ, `<?xml version="1.0"?>`, `make_root()`, `serialize()`, `sub()`.
6. ✅ `render.py` — Jinja2 environment с `env` глобалом и `load_yaml`; рендер в строку + сохранение промежуточного `config.yaml`.
7. ✅ `build.py` — главный пайплайн (рендер → YAML → pydantic → builders → XML).
8. ✅ `cli.py` — argparse CLI с командой `render`.
9. ✅ `__main__.py` — `python -m opnsense_config_generator`.

### Этап 2 — pydantic-модели и builders для базовых секций (MVP) ✅

Каждая секция = pydantic-модель в `models/` + builder в `builders/`.

1. ✅ `system` — hostname, domain, dns, timezone, webgui, ssh, users (bcrypt), groups
2. ✅ `interfaces` — assignments (wan/lan/opt), IPv4/IPv6, track6, DHCP6
3. ✅ `vlans`, `bridges`, `laggs`
4. ✅ `gateways` + `staticroutes`
5. ✅ `aliases` — host, network, port, url, urltable, geoip, …
6. ✅ `filter` — правила (pass/block/reject), source/dest с any/network/address/port, tracker UUID
7. ✅ `nat` — outbound (automatic/hybrid/advanced), port forward, 1:1
8. ✅ `dhcpd` — legacy ISC DHCP; static maps, range, DNS/NTP опции
   — *Kea: отложено до Этапа 4 (в OPNsense 26.1 по умолчанию всё ещё ISC DHCP)*
9. ✅ `unbound` — DNSSEC, forwarding, host/domain overrides, custom_options

### Этап 3 — golden-тесты и MVP ✅

1. ✅ `tests/golden/minimal/config.yaml` — минимальная конфигурация (LAN+WAN, правила, DHCP, DNS).
2. ✅ `tests/test_xml_wellformed.py` — well-formed XML, корень `<opnsense>`, версия, bcrypt, секции.
3. ✅ `tests/test_golden.py` — golden-тест с нормализацией timestamp/bcrypt.
4. ✅ `tests/test_snapshots.py` — snapshot-тесты по секциям (system, interfaces, filter).
5. ✅ `tests/unit/` — 20 unit-тестов: uuid, password, revision, render, models validation.
6. ✅ Рефакторинг структуры: `templates/config.yaml.j2` → `config.yaml.j2` (корень); `examples/` → удалён; добавлен `docs/` с `minimal_config.yaml.j2` и `full_config.yaml.j2`; заполнен `README.md`.
7. ✅ Smoke-тест вручную: импорт `tests/golden/minimal/config.yaml` → `config.xml` → загрузка в OPNsense. Успешно.
8. 🔲 Релиз 0.1.0 (тег).

### Этап 4 — расширенные секции ✅

1. ✅ `ntpd` — legacy-секция; модель + builder + snapshot-тест
2. ✅ `cert`, `ca` (PKI / Trust) — модели + builder (refid детерминированный через uuid5)
3. ✅ `syslog` (MVC `//OPNsense/Syslog`) — модель + builder + snapshot-тест
4. ✅ `wireguard` (MVC: General, Server, Client) — модель + builder + snapshot-тест; peers резолвятся по имени в UUID
5. ✅ `openvpn` (MVC `//OPNsense/OpenVPN`) — модель + builder + snapshot-тест (Instances, StaticKeys, Overwrites)
6. ✅ `ipsec` (MVC `//OPNsense/Swanctl`) — модель + builder + snapshot-тест (Connections, locals, remotes, children, Pools)
7. ✅ `build.py` расширен: `<OPNsense>` MVC-контейнер, legacy cert/ca/ntpd напрямую под `<opnsense>`
8. ✅ `tests/golden/typical/config.yaml` + `expected.xml` — golden-тест с WireGuard + cert/ca + ntpd + syslog
   **Итого: 42 теста, все зелёные.**

---

#### Шаблон реализации для этапов 5–14

**Паттерн одного этапа** (взят из реализации qemu-guest-agent, Этап 14):

```
models/<plugin>.py   — pydantic-контракт YAML
builders/<plugin>.py — lxml builder, возвращает None если не enabled
tests/snapshots/<plugin>/basic.yaml + basic.expected.xml
tests/snapshots/<plugin>/with_<variant>.yaml + with_<variant>.expected.xml  (если нужен)
```

Интеграция в `build.py`:
- Секции из `opnsense/core` (`monit`, `cron`, `TrafficShaper`, `Kea`) → в список MVC-блока под `<OPNsense>`
- Секции из `opnsense/plugins` с mount `//OPNsense/...` → тоже под `<OPNsense>`
- Секции с mount `//system/...` → **legacy**, добавляются напрямую под `<opnsense>` (как ntpd/cert/ca)

Как скачать MVC-модель плагина из `opnsense/plugins`:
```
# Найти путь: API tree
curl "https://api.github.com/repos/opnsense/plugins/git/trees/HEAD?recursive=1" | python3 -c "
import sys,json; [print(x['path']) for x in json.load(sys.stdin)['tree'] if 'models/OPNsense' in x['path'] and x['path'].endswith('.xml')]
"
# Скачать файл:
curl "https://raw.githubusercontent.com/opnsense/plugins/master/<path>"
```

Тег `<mount>` внутри XML-модели указывает куда писать в config.xml:
- `//OPNsense/Foo` → `<OPNsense><Foo>...` (MVC-блок)
- `//system/bar` → `<system><bar>...` (legacy, напрямую под `<opnsense>`)

---

### Этап 5 — monit (MVC) 🔲

Источник: `opnsense/core`, модель уже в `opnsense_reference/mvc_models/Monit/Monit.xml`
Mount: `//OPNsense/monit` → XML-элемент `<monit>` под `<OPNsense>`

1. 🔲 Изучить `opnsense_reference/mvc_models/Monit/Monit.xml` (General, Service, Test, Alert — ArrayField-секции)
2. 🔲 pydantic-модель `models/monit.py` — General, Services, Tests, Alerts
3. 🔲 Builder `builders/monit.py` → `<monit>` под `<OPNsense>`
4. 🔲 Snapshot-тест `tests/snapshots/monit/`
5. 🔲 Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 6 — cron (MVC) 🔲

Источник: `opnsense/core`, модель уже в `opnsense_reference/mvc_models/Cron/Cron.xml`
Mount: `//OPNsense/cron` → XML-элемент `<cron>` под `<OPNsense>`

1. 🔲 Изучить `opnsense_reference/mvc_models/Cron/Cron.xml` (jobs — ArrayField)
2. 🔲 pydantic-модель `models/cron.py` — Jobs (команда, минуты/часы/дни, enabled)
3. 🔲 Builder `builders/cron.py` → `<cron>` под `<OPNsense>`
4. 🔲 Snapshot-тест `tests/snapshots/cron/`
5. 🔲 Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 7 — trafficshaper / QoS (MVC) 🔲

Источник: `opnsense/core`, модель уже в `opnsense_reference/mvc_models/TrafficShaper/TrafficShaper.xml`
Mount: `//OPNsense/TrafficShaper` → XML-элемент `<TrafficShaper>` под `<OPNsense>`

1. 🔲 Изучить `opnsense_reference/mvc_models/TrafficShaper/TrafficShaper.xml` (Pipe, Queue, Rule — ArrayField)
2. 🔲 pydantic-модель `models/trafficshaper.py` — Pipes, Queues, Rules
3. 🔲 Builder `builders/trafficshaper.py` → `<TrafficShaper>` под `<OPNsense>`
4. 🔲 Snapshot-тест `tests/snapshots/trafficshaper/`
5. 🔲 Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 8 — radvd (MVC) ✅

Источник: `opnsense/core`, модель `src/opnsense/mvc/app/models/OPNsense/Radvd/Radvd.xml`
Mount: `//OPNsense/radvd` → XML-элемент `<radvd>` под `<OPNsense>`
XML структура: `<radvd><entries uuid="...">...</entries></radvd>` (direct children, нет обёртки)

1. ✅ Скачать MVC-модель → `opnsense_reference/mvc_models/Radvd/Radvd.xml`
2. ✅ pydantic-модель `models/radvd.py` — RadvdEntry (interface required, mode, rdnss, dnssl, routes, таймеры) + RadvdConfig
3. ✅ Builder `builders/radvd.py` → `<radvd>` под `<OPNsense>` (None если entries пусто)
4. ✅ Snapshot fixture `tests/snapshots/radvd/basic.yaml` (2 entries: lan stateless с RDNSS/DNSSL, opt1 managed disabled)
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок) + `test_snapshots.py` + `test_models_validation.py`
✅ Запущены тесты, сгенерирован `basic.expected.xml`, 76 тестов зелёных

### Этап 9 — Kea DHCP v4/v6 (MVC) ✅

Источник: `opnsense/core`, модели уже в `opnsense_reference/mvc_models/Kea/`
Файлы: `KeaDhcpv4.xml`, `KeaDhcpv6.xml`, `KeaCtrlAgent.xml`, `KeaDdns.xml`
Mounts: `//OPNsense/Kea/dhcp4`, `//OPNsense/Kea/dhcp6`, `//OPNsense/Kea/ctrl_agent`, `//OPNsense/Kea/ddns`

1. ✅ Изучить все 4 XML-модели Kea
2. ✅ pydantic-модель `models/kea.py` — DHCPv4/v6: general, subnets (pools, option_data), reservations; CtrlAgent; DDNS
3. ✅ Builder `builders/kea.py` → `<Kea>` под `<OPNsense>` (4 субэлемента: dhcp4, dhcp6, ctrl_agent, ddns)
4. ✅ Snapshot-тесты: `basic` (dhcp4 + subnet) и `with_reservations` (+ static maps)
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок)
   **Итого: 53 теста, все зелёные.**

### Этап 10 — os-acme-client (MVC) ✅

Плагин: `os-acme-client 4.15` — Let's Encrypt / ACME-клиент.
Mount: `//OPNsense/AcmeClient` → `<AcmeClient>` под `<OPNsense>`
Модели: AcmeSettings, AcmeAccount, AcmeCertificate, AcmeValidation (dns_credentials dict), AcmeAction (extra_params dict)
Cross-references: certificate.account/validationMethod/restartActions → UUIDs по name

1. ✅ Скачать `AcmeClient.xml` → `opnsense_reference/mvc_models/AcmeClient/`
2. ✅ pydantic-модель `models/acme_client.py`
3. ✅ Builder `builders/acme_client.py` → `<AcmeClient>` под `<OPNsense>`
4. ✅ Snapshot-тест `tests/snapshots/acme_client/basic.yaml` + `basic.expected.xml`
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 11 — os-bind (MVC) ✅

Плагин: `os-bind 1.34_2` — BIND DNS authoritative/recursive сервер.
5 mount-точек объединены в `<bind>`: general, acl, domain, record, dnsbl
Cross-references: general.recursion/allowtransfer/allowquery → ACL UUIDs; record.domain → Domain UUID

1. ✅ Скачать все 5 XML-моделей → `opnsense_reference/mvc_models/Bind/`
2. ✅ pydantic-модель `models/bind.py` — BindGeneral, BindAcl, BindDomain, BindRecord, BindDnsbl, BindConfig
3. ✅ Builder `builders/bind.py` → `<bind>` под `<OPNsense>`
4. ✅ Snapshot-тест `tests/snapshots/bind/basic.yaml` + `basic.expected.xml`
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 12 — os-chrony (MVC) ✅

Плагин: `os-chrony 1.5_3` — NTP через Chrony.
Mount: `//OPNsense/chrony/general` → `<chrony><general>` под `<OPNsense>`

1. ✅ Скачать `General.xml` → `opnsense_reference/mvc_models/Chrony/`
2. ✅ pydantic-модель `models/chrony.py` — ChronyGeneral (enabled, port, nts_client, peers, allowed_networks), ChronyConfig
3. ✅ Builder `builders/chrony.py` → `<chrony><general>` под `<OPNsense>` (None если не enabled)
4. ✅ Snapshot-тест `tests/snapshots/chrony/basic.yaml` + `basic.expected.xml`
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок)

### Этап 13 — os-git-backup (legacy mount) ✅

Плагин: `os-git-backup 1.1_3` — автоматический git-бэкап конфигурации.
Mount: `//system/backup/git` → LEGACY: `<system><backup><git>` (не под `<OPNsense>`)
Интеграция: в `build.py` builder возвращает `<git>`, оборачивается в `<backup>` и добавляется в `<system>`

1. ✅ Скачать `GitSettings.xml` → `opnsense_reference/mvc_models/GitBackup/`
2. ✅ pydantic-модель `models/git_backup.py` — enabled, url, branch, force_push, privkey, user, password
3. ✅ Builder `builders/git_backup.py` → `<git>` (None если не enabled)
4. ✅ Snapshot-тест `tests/snapshots/git_backup/basic.yaml` + `basic.expected.xml`
5. ✅ Интеграция в `build.py`: `<backup><git>` вставляется в `<system>` перед его добавлением в root

### Этап 14 — os-qemu-guest-agent (MVC) ✅

Плагин: `os-qemu-guest-agent 1.3` — QEMU Guest Agent для виртуальных машин.

1. ✅ MVC-модель плагина (`OPNsense/QemuGuestAgent/QemuGuestAgent.xml`) → `opnsense_reference/mvc_models/QemuGuestAgent/`
2. ✅ pydantic-модель `models/qemu_guest_agent.py` — General: enabled, log_debug, disabled_rpcs (Literal)
3. ✅ Builder `builders/qemu_guest_agent.py` → `<OPNsense><QemuGuestAgent>` (None если disabled)
4. ✅ Snapshot-тесты: `basic` (enable only) и `with_disabled_rpcs` (debug + RPCs)
5. ✅ Интеграция в `models/root.py` + `build.py` (MVC-блок)
   **Итого: 48 тестов, все зелёные.**

### Этап 15 — документированные шаблоны (обновление) 🔲

После завершения этапов 5–14:

- ✅ `config.yaml.j2` (корень) — рабочий шаблон: минимальная конфигурация, краткие комментарии
- ✅ `docs/minimal_config.yaml.j2` — справочник: основные секции, соответствует default_config.xml OPNsense 26.x
- ✅ `docs/full_config.yaml.j2` — справочник: все секции этапов 0–4 (system, interfaces, vlans, bridges, laggs, gateways, staticroutes, aliases, filter, nat, dnsmasq, unbound, ntpd, certs, wireguard, openvpn, ipsec, syslog)
- ✅ `README.md` — полное описание проекта и инструкция по использованию
- 🔲 Дополнить `docs/full_config.yaml.j2` секциями этапов 5–14 (monit, cron, trafficshaper, radvd, Kea, ACME, BIND, Chrony, GitBackup, QemuGuestAgent)

### Этап 16 — финализация 🔲

1. 🔲 `tests/golden/full/` — полная конфигурация со всеми поддерживаемыми секциями
2. 🔲 Финальный smoke-тест на живой OPNsense
3. 🔲 Релиз 1.0.0

### Этап 17 — отложенное 🔲

1. 🔲 Поддержка secrets (через env / `secrets.yaml`).
2. 🔲 Docker-обёртка (Dockerfile + docker-compose пример).
3. 🔲 CI workflow (GitHub Actions): ruff, mypy, pytest на push.
4. 🔲 Cron-job для `check_new_opnsense_release.py`.

---

## 14. Зафиксированные решения (быстрая сводка)

| Решение | Значение |
|---|---|
| Сценарий | One-shot import |
| Поток | yaml.j2 → yaml (на диск) → xml |
| Версия Python | 3.12+ |
| Менеджер пакетов | pip + requirements*.txt |
| Версия OPNsense | последняя стабильная community |
| Имя пакета | `opnsense_config_generator` |
| Контракт YAML | pydantic v2, строгий |
| DSL-абстракции | нет, 1:1 маппинг в XML |
| UUID | uuid5(NAMESPACE, "section:name"), детерминированно |
| Revision | фиксированный блок при рендере |
| Пароли | plaintext в YAML → bcrypt-хэш в XML |
| Round-trip | не нужен |
| Линтер | ruff |
| Типизация | mypy strict + pydantic.mypy |
| Тесты | pytest + unit + snapshot + golden + xml-wellformed |
| Docker | отложено |
| Secrets | отложено |
