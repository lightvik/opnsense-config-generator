from pydantic import BaseModel, Field


class Bridge(BaseModel):
    bridgeif: str
    members: list[str] = Field(default_factory=list)
    descr: str = ""
    stp: bool = False
    rstp: bool = False
    maxaddr: int = 100
    timeout: int = 240


class BridgesConfig(BaseModel):
    bridges: list[Bridge] = Field(default_factory=list)
