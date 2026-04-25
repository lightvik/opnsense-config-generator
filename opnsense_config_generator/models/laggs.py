from typing import Literal

from pydantic import BaseModel, Field


class Lagg(BaseModel):
    laggif: str
    proto: Literal["lacp", "failover", "loadbalance", "roundrobin", "none"] = "lacp"
    members: list[str] = Field(default_factory=list)
    descr: str = ""
    laggport: list[str] = Field(default_factory=list)


class LaggsConfig(BaseModel):
    laggs: list[Lagg] = Field(default_factory=list)
