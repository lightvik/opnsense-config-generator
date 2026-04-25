from typing import Literal

from pydantic import BaseModel, Field

QemuRpc = Literal[
    "guest-exec",
    "guest-exec-status",
    "guest-file-close",
    "guest-file-flush",
    "guest-file-open",
    "guest-file-read",
    "guest-file-seek",
    "guest-file-write",
    "guest-fsfreeze-freeze",
    "guest-fsfreeze-freeze-list",
    "guest-fsfreeze-status",
    "guest-fsfreeze-thaw",
    "guest-fstrim",
    "guest-get-fsinfo",
    "guest-get-host-name",
    "guest-get-memory-block-info",
    "guest-get-memory-blocks",
    "guest-get-osinfo",
    "guest-get-time",
    "guest-get-timezone",
    "guest-get-users",
    "guest-get-vcpus",
    "guest-info",
    "guest-network-get-interfaces",
    "guest-ping",
    "guest-set-memory-blocks",
    "guest-set-time",
    "guest-set-user-password",
    "guest-set-vcpus",
    "guest-shutdown",
    "guest-suspend-disk",
    "guest-suspend-hybrid",
    "guest-suspend-ram",
    "guest-sync",
    "guest-sync-delimited",
]


class QemuGuestAgentConfig(BaseModel):
    enabled: bool = False
    log_debug: bool = False
    disabled_rpcs: list[QemuRpc] = Field(default_factory=list)
