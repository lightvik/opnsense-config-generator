# AI Disclosure

This project was created with the assistance of **Claude** — an AI assistant made by [Anthropic](https://www.anthropic.com).

## What Claude helped with

The entire project was designed and implemented in collaboration with Claude:

- Architecture: Jinja2 → Pydantic → lxml pipeline for generating OPNsense config.xml
- All Python source files: Pydantic models, XML builders, CLI, utilities
- 28 supported configuration sections across all OPNsense subsystems
- Snapshot and golden test infrastructure
- Docker support
- Reference documentation (`docs/full_config.yaml.j2`, `docs/minimal_config.yaml.j2`)
- Documentation (`README.md`)

## About Claude

Claude is a large language model trained by Anthropic to be helpful, harmless, and honest.
It can reason about code, architecture, and trade-offs — and holds a conversation while doing it.

Models used: **Claude Opus 4** for planning and architecture decisions, **Claude Sonnet 4.6** for implementation.

More at: [anthropic.com/claude](https://www.anthropic.com/claude)
