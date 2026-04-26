import textwrap
from pathlib import Path

import pytest

from opnsense_config_generator.render import render_template


def test_render_simple_template(tmp_path: Path) -> None:
    template = tmp_path / "tpl" / "config.yaml.j2"
    template.parent.mkdir()
    template.write_text("hostname: myfw\n")
    intermediate = tmp_path / "out.yaml"
    result = render_template(template, intermediate)
    assert result["hostname"] == "myfw"
    assert intermediate.read_text() == "hostname: myfw\n"


def test_render_env_variable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_HOST", "envfw")
    template = tmp_path / "tpl" / "config.yaml.j2"
    template.parent.mkdir()
    template.write_text("hostname: {{ env.MY_HOST }}\n")
    result = render_template(template, tmp_path / "out.yaml")
    assert result["hostname"] == "envfw"


def test_render_env_get_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MISSING_VAR", raising=False)
    template = tmp_path / "tpl" / "config.yaml.j2"
    template.parent.mkdir()
    template.write_text("hostname: {{ env.get('MISSING_VAR', 'default_host') }}\n")
    result = render_template(template, tmp_path / "out.yaml")
    assert result["hostname"] == "default_host"


def test_render_load_yaml(tmp_path: Path) -> None:
    extra = tmp_path / "extra.yaml"
    extra.write_text("dns: 8.8.8.8\n")
    template = tmp_path / "tpl" / "config.yaml.j2"
    template.parent.mkdir()
    template.write_text(
        textwrap.dedent(f"""\
        {{% set data = load_yaml('{extra}') %}}
        dns: {{{{ data.dns }}}}
        """)
    )
    result = render_template(template, tmp_path / "out.yaml")
    assert result["dns"] == "8.8.8.8"
