import os
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


def _make_env(template_dir: Path) -> Environment:
    jinja_env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    jinja_env.globals["env"] = os.environ

    def load_yaml(path: str) -> Any:
        return yaml.safe_load(Path(path).read_text())

    jinja_env.globals["load_yaml"] = load_yaml
    return jinja_env


def render_template(template_path: Path, intermediate_path: Path) -> dict[str, Any]:
    jinja_env = _make_env(template_path.parent)
    rendered = jinja_env.get_template(template_path.name).render()
    intermediate_path.parent.mkdir(parents=True, exist_ok=True)
    intermediate_path.write_text(rendered)
    result: dict[str, Any] = yaml.safe_load(rendered) or {}
    return result
