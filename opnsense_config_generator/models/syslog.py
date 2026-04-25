from typing import Literal

from pydantic import BaseModel, Field

SyslogTransport = Literal["udp4", "tcp4", "udp6", "tcp6", "tls4", "tls6"]
SyslogLevel = Literal["debug", "info", "notice", "warn", "err", "crit", "alert", "emerg"]


class SyslogGeneral(BaseModel):
    enabled: bool = True
    loglocal: bool = True
    maxpreserve: int = 31
    maxfilesize: int | None = None


class SyslogDestination(BaseModel):
    enabled: bool = True
    transport: SyslogTransport = "udp4"
    hostname: str
    port: int = 514
    rfc5424: bool = False
    level: list[str] = Field(default_factory=list)
    facility: list[str] = Field(default_factory=list)
    program: list[str] = Field(default_factory=list)
    certificate: str = ""  # certref (for TLS transport)
    description: str = ""


class SyslogConfig(BaseModel):
    general: SyslogGeneral = Field(default_factory=SyslogGeneral)
    destinations: list[SyslogDestination] = Field(default_factory=list)
