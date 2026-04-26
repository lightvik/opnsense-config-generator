#!/usr/bin/env python3
"""Check GitHub for new stable OPNsense CE releases (for CI cron-job)."""

import json
import os
import sys
import urllib.request
from pathlib import Path

REFERENCE_DIR = Path(__file__).parent.parent / "opnsense_reference"
API_URL = "https://api.github.com/repos/opnsense/core/releases?per_page=20"


def get_current_version() -> str:
    version_file = REFERENCE_DIR / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return ""


def get_latest_stable() -> str | None:
    headers = {
        "User-Agent": "opnsense-config-generator/check",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(API_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        releases = json.loads(resp.read())

    for rel in releases:
        if rel.get("prerelease") or rel.get("draft"):
            continue
        tag = rel.get("tag_name", "")
        # OPNsense stable tags look like "26.1.6" or "v26.1.6"
        version = tag.lstrip("v")
        parts = version.split(".")
        if len(parts) >= 2:
            return version
    return None


def main() -> None:
    current = get_current_version()
    latest = get_latest_stable()
    if latest is None:
        print("Could not determine latest release", file=sys.stderr)
        sys.exit(1)

    print(f"Current pinned: {current or '(none)'}")
    print(f"Latest stable:  {latest}")

    if current and latest.startswith(current.rsplit(".", 1)[0]):
        print("Up to date.")
        sys.exit(0)

    print(f"NEW RELEASE DETECTED: {latest} (pinned: {current})")
    print("Run: python scripts/sync_opnsense_reference.py --tag stable/<major.minor>")
    sys.exit(2)


if __name__ == "__main__":
    main()
