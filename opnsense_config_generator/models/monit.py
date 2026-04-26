from typing import Literal

from pydantic import BaseModel, Field

SslVersion = Literal["auto", "tlsv1", "tlsv11", "tlsv12", "tlsv13"]
ServiceType = Literal[
    "process", "file", "fifo", "filesystem", "directory", "host", "system", "custom", "network"
]
TestType = Literal[
    "Existence", "SystemResource", "ProcessResource", "ProcessDiskIO", "FileChecksum",
    "Timestamp", "FileSize", "FileContent", "FilesystemMountFlags", "SpaceUsage",
    "InodeUsage", "DiskIO", "Permisssion", "UID", "GID", "PID", "PPID", "Uptime",
    "ProgramStatus", "NetworkInterface", "NetworkPing", "Connection", "Custom",
]
TestAction = Literal["alert", "restart", "start", "stop", "exec", "unmonitor"]


class MonitGeneral(BaseModel):
    enabled: bool = False
    interval: int = 120
    startdelay: int = 120
    mailserver: str = "127.0.0.1"
    port: int = 25
    username: str = ""
    password: str = ""
    ssl: bool = False
    sslversion: SslVersion = "auto"
    sslverify: bool = True
    logfile: str = ""
    statefile: str = ""
    eventqueue_path: str = ""
    eventqueue_slots: int | None = None
    httpd_enabled: bool = False
    httpd_username: str = "root"
    httpd_password: str = ""
    httpd_port: int = 2812
    httpd_allow: list[str] = Field(default_factory=list)
    mmonit_url: str = ""
    mmonit_timeout: int = 5
    mmonit_register_credentials: bool = True


class MonitAlert(BaseModel):
    enabled: bool = False
    recipient: str = "root@localhost.local"
    noton: bool = False
    events: list[str] = Field(default_factory=list)
    format: str = ""
    reminder: int | None = None
    description: str = ""


class MonitService(BaseModel):
    enabled: bool = False
    name: str
    description: str = ""
    type: ServiceType
    pidfile: str = ""
    match: str = ""
    path: str = ""
    timeout: int = 300
    starttimeout: int = 30
    address: str = ""
    interface: str = ""
    start: str = ""
    stop: str = ""
    tests: list[str] = Field(default_factory=list)   # test names → resolved to UUIDs in builder
    depends: list[str] = Field(default_factory=list)  # service names → resolved to UUIDs in builder
    polltime: str = ""


class MonitTest(BaseModel):
    name: str
    type: TestType = "Custom"
    condition: str
    action: TestAction
    path: str = ""


class MonitConfig(BaseModel):
    general: MonitGeneral = Field(default_factory=MonitGeneral)
    alerts: list[MonitAlert] = Field(default_factory=list)
    services: list[MonitService] = Field(default_factory=list)
    tests: list[MonitTest] = Field(default_factory=list)
