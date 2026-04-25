import argparse
import sys
from pathlib import Path

from opnsense_config_generator.build import run_pipeline
from opnsense_config_generator.version import OPNSENSE_VERSION, TOOL_VERSION


def _render_cmd(args: argparse.Namespace) -> None:
    run_pipeline(
        template_path=Path(args.template),
        intermediate_path=Path(args.intermediate),
        output_path=Path(args.output),
    )
    print(f"Generated: {args.output}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="opnsense-config-generator",
        description=(
            f"OPNsense config.xml generator v{TOOL_VERSION} "
            f"(target OPNsense {OPNSENSE_VERSION})"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    render = sub.add_parser("render", help="Render template to config.xml")
    render.add_argument(
        "--template",
        default="config.yaml.j2",
        help="Path to Jinja2 template (default: config.yaml.j2)",
    )
    render.add_argument(
        "--intermediate",
        default="build/config.yaml",
        help="Path to save intermediate YAML (default: build/config.yaml)",
    )
    render.add_argument(
        "--output",
        default="build/config.xml",
        help="Path to write config.xml (default: build/config.xml)",
    )
    render.set_defaults(func=_render_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())  # type: ignore[func-returns-value]
