from typing import Literal

from pydantic import BaseModel, Field

AliasType = Literal[
    "host",
    "network",
    "port",
    "url",
    "urltable",
    "geoip",
    "networkgroup",
    "mac",
    "asn",
    "dynipv6host",
    "authgroup",
    "internal",
    "external",
]


class Alias(BaseModel):
    name: str
    type: AliasType
    descr: str = ""
    content: list[str] = Field(default_factory=list)
    enabled: bool = True
    proto: str = ""
    # urltable refresh interval (hours)
    updatefreq: float = 0.0
    counters: bool = False
    interface: str = ""


class AliasesConfig(BaseModel):
    aliases: list[Alias] = Field(default_factory=list)
