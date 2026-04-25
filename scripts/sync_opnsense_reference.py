#!/usr/bin/env python3
"""Download OPNsense reference files from GitHub for a given tag/branch."""

import argparse
import sys
import urllib.request
from pathlib import Path

REPO = "opnsense/core"
BASE_URL = "https://raw.githubusercontent.com/{repo}/{ref}/{path}"

REFERENCE_DIR = Path(__file__).parent.parent / "opnsense_reference"

# Files to download: (repo_path, local_relative_path)
CORE_FILES = [
    ("src/etc/config.xml.sample", "default_config.xml"),
]

# MVC model files: (plugin_dir, model_filename)
MVC_MODELS = [
    ("Wireguard", "General.xml"),
    ("Wireguard", "Server.xml"),
    ("Wireguard", "Client.xml"),
    ("Kea", "KeaDhcpv4.xml"),
    ("Kea", "KeaDhcpv6.xml"),
    ("Kea", "KeaCtrlAgent.xml"),
    ("Kea", "KeaDdns.xml"),
    ("CaptivePortal", "CaptivePortal.xml"),
    ("IPsec", "Swanctl.xml"),
    ("OpenVPN", "OpenVPN.xml"),
    ("Unbound", "Unbound.xml"),
    ("Firewall", "Alias.xml"),
    ("Firewall", "Filter.xml"),
    ("Interfaces", "Vip.xml"),
    ("Routes", "Route.xml"),
    ("Cron", "Cron.xml"),
    ("Monit", "Monit.xml"),
    ("Syslog", "Syslog.xml"),
    ("TrafficShaper", "TrafficShaper.xml"),
    ("Trust", "Ca.xml"),
    ("Trust", "Cert.xml"),
    ("Trust", "General.xml"),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "opnsense-config-generator/sync"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as e:
        print(f"  WARN: {url} — {e}", file=sys.stderr)
        return b""


def sync(ref: str) -> None:
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    (REFERENCE_DIR / "mvc_models").mkdir(exist_ok=True)

    print(f"Syncing OPNsense reference for ref={ref!r} ...")

    for repo_path, local_name in CORE_FILES:
        url = BASE_URL.format(repo=REPO, ref=ref, path=repo_path)
        print(f"  {repo_path} ...", end=" ", flush=True)
        data = fetch(url)
        if data:
            (REFERENCE_DIR / local_name).write_bytes(data)
            print("OK")
        else:
            print("SKIP")

    for plugin, model_file in MVC_MODELS:
        repo_path = f"src/opnsense/mvc/app/models/OPNsense/{plugin}/{model_file}"
        local_dir = REFERENCE_DIR / "mvc_models" / plugin
        local_dir.mkdir(exist_ok=True)
        url = BASE_URL.format(repo=REPO, ref=ref, path=repo_path)
        print(f"  {plugin}/{model_file} ...", end=" ", flush=True)
        data = fetch(url)
        if data:
            (local_dir / model_file).write_bytes(data)
            print("OK")
        else:
            print("SKIP")

    version_str = ref.lstrip("v")
    (REFERENCE_DIR / "VERSION").write_text(version_str + "\n")
    print(f"Done. VERSION={version_str}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync OPNsense reference files")
    parser.add_argument(
        "--tag",
        "--ref",
        dest="ref",
        default="26.1.6",
        help="Git tag or branch (e.g. 26.1.6, stable/26.1)",
    )
    args = parser.parse_args()
    sync(args.ref)


if __name__ == "__main__":
    main()
