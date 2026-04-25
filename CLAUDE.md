# CLAUDE.md — opnsense-config-generator

This file tells Claude which context files to read for common tasks.
All context files are in `context/`. Read only what's relevant.

## Task routing

### Adding a new plugin/section

Read:
- [context/builder_pattern.md](context/builder_pattern.md) — how to write model + builder
- [context/uuid_pattern.md](context/uuid_pattern.md) — deterministic UUIDs and cross-references
- [context/testing.md](context/testing.md) — how to add snapshot test
- [context/stages.md](context/stages.md) — where to register in build.py and root.py
- [context/xml_api.md](context/xml_api.md) — helpers reference

### Fixing or adding tests

Read:
- [context/testing.md](context/testing.md) — snapshot, unit, golden test patterns

### Understanding the XML output structure

Read:
- [context/architecture.md](context/architecture.md) — pipeline and XML layout

### Finding where a section is implemented

Read:
- [context/stages.md](context/stages.md) — field → builder → file mapping

### Working with UUIDs or cross-references

Read:
- [context/uuid_pattern.md](context/uuid_pattern.md)

### Reviewing helpers / low-level XML API

Read:
- [context/xml_api.md](context/xml_api.md)

## Quick reference

- Run tests: `.venv/bin/python -m pytest`
- Regenerate snapshots: `.venv/bin/python -m pytest --update-snapshots`
- Root model: `opnsense_config_generator/models/root.py`
- Build orchestrator: `opnsense_config_generator/build.py`
- OPNsense reference XML: `opnsense_reference/default_config.xml`
