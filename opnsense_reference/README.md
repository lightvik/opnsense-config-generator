# OPNsense Reference Files

This directory contains reference files from the OPNsense upstream repository,
pinned to the version in `VERSION`.

## Updating

When a new stable OPNsense CE release is out:

```bash
# Check if there is a new release
python scripts/check_new_opnsense_release.py

# Download reference files for the new version
python scripts/sync_opnsense_reference.py --tag stable/26.1
```

Then:
1. Review `git diff opnsense_reference/` for structural changes.
2. Update pydantic models and builders if sections changed.
3. Re-run golden tests: `pytest tests/test_golden.py --update-snapshots`.
4. Fix any regressions.
5. Bump `OPNSENSE_VERSION` in `opnsense_config_generator/version.py`.
6. Commit and release.

## Contents

- `VERSION` — pinned OPNsense version (e.g. `26.1`)
- `default_config.xml` — `src/etc/config.xml` from opnsense/core
- `mvc_models/<Plugin>/<Model>.xml` — formal MVC model definitions for plugins
