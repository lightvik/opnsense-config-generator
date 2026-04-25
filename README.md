# opnsense-config-generator

Генерирует `config.xml` для OPNsense из Jinja2-шаблона. Один раз отредактировать файл,
получить готовый XML для импорта — без ручной настройки через веб-интерфейс.

Целевая версия: **OPNsense 26.1**

## Версионирование

Тег релиза содержит обе версии: `opnsense-{OPNSENSE_VERSION}_v{TOOL_VERSION}`.

Текущий тег: `opnsense-26.1.6_v0.0.1`

- При обновлении до новой версии OPNsense — обновляется `OPNSENSE_VERSION` в `version.py` и создаётся новый тег.
- При изменениях только в инструменте — инкрементируется `TOOL_VERSION`, `OPNSENSE_VERSION` не меняется.

## Как это работает

```text
config.yaml.j2  →  (Jinja2 render)  →  build/config.yaml  →  (XML builder)  →  build/config.xml
```

1. Отредактируйте `config.yaml.j2` в корне рабочей директории
2. Запустите генератор
3. Импортируйте `build/config.xml` в OPNsense:
   **System → Configuration → Backups → Restore**

## Использование

### Docker (рекомендуется)

```bash
docker run --rm --volume "$(pwd):/work" opnsense-config-generator
```

С явными путями:

```bash
docker run --rm --volume "$(pwd):/work" opnsense-config-generator render \
    --template config.yaml.j2 \
    --intermediate build/config.yaml \
    --output build/config.xml
```

### Локально

Требуется **Python 3.12+**.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

opnsense-config-generator render
```

### Параметры команды `render`

| Параметр         | По умолчанию        | Описание                         |
|------------------|---------------------|----------------------------------|
| `--template`     | `config.yaml.j2`    | Jinja2-шаблон                    |
| `--intermediate` | `build/config.yaml` | Промежуточный YAML (для отладки) |
| `--output`       | `build/config.xml`  | Итоговый config.xml              |

## Шаблон

Рабочий шаблон — `config.yaml.j2` в текущей директории. Содержит минимальную рабочую
конфигурацию: WAN/LAN, пользователь root, DHCP, DNS, базовые правила фаервола.

Справочная документация:

| Файл                          | Описание                                                |
| ----------------------------- | ------------------------------------------------------- |
| `docs/minimal_config.yaml.j2` | Только основные секции, все параметры задокументированы |
| `docs/full_config.yaml.j2`    | Все секции со всеми параметрами и примерами             |

### Возможности Jinja2

```yaml
# Переменные окружения
hostname: {{ env.MY_HOSTNAME | default('fw01') }}

# Загрузка внешнего YAML (например, секреты)
{% set sec = load_yaml('/etc/opnsense-secrets.yaml') %}
password: {{ sec.admin_password }}

# Условия
{% if env.get('ENABLE_SSH') == '1' %}
ssh:
  enabled: true
{% endif %}
```

## Поддерживаемые секции

| Секция | Описание |
| --- | --- |
| `system` | Hostname, DNS, NTP, пользователи, группы, WebGUI, SSH |
| `interfaces` | WAN, LAN, OPT-интерфейсы (static / DHCP / PPPoE) |
| `vlans` | 802.1Q VLAN |
| `bridges` | Bridge-интерфейсы |
| `laggs` | Link aggregation (LACP / failover) |
| `gateways` | Определения шлюзов |
| `staticroutes` | Статические маршруты |
| `aliases` | Алиасы фаервола (host / network / port / URL) |
| `certs` | CA и TLS-сертификаты |
| `filter` | Правила фаервола |
| `nat` | Outbound NAT, port forwarding, 1:1 NAT |
| `unbound` | DNS-резолвер, host overrides, domain overrides |
| `dnsmasq` | Лёгкий DNS/DHCP (dnsmasq) |
| `ntpd` | NTP-сервер |
| `wireguard` | WireGuard VPN |
| `openvpn` | OpenVPN (сервер и клиент) |
| `ipsec` | IPsec / IKEv2 |
| `syslog` | Удалённый syslog |
| `cron` | Задачи по расписанию |
| `monit` | Мониторинг сервисов (Monit) |
| `trafficshaper` | Traffic shaping (HFSC / PRIQ / FAIRQ) |
| `radvd` | Router Advertisement (IPv6) |
| `kea` | Kea DHCP (v4 / v6) |
| `acme_client` | ACME / Let's Encrypt сертификаты |
| `bind` | BIND DNS-сервер |
| `chrony` | Chrony NTP |
| `qemu_guest_agent` | QEMU Guest Agent |
| `git_backup` | Резервное копирование конфига в Git |

## Разработка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .

ruff check .
ruff format --check .
mypy opnsense_config_generator
pytest
```

Обновить ожидаемые снимки тестов после изменений:

```bash
pytest --update-snapshots
```

## Обновление референсных файлов OPNsense

```bash
python scripts/sync_opnsense_reference.py
```

Скачивает `config.xml.sample` и MVC-модели для зафиксированной версии OPNsense из GitHub.
Версия зафиксирована в `opnsense_config_generator/version.py`.
