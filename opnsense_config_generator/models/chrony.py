from pydantic import BaseModel, Field


class ChronyGeneral(BaseModel):
    enabled: bool = False
    port: int = 323
    nts_client: bool = False
    ntsnocert: bool = False
    peers: list[str] = Field(default_factory=lambda: ["0.opnsense.pool.ntp.org"])
    fallback_peers: str = ""
    allowed_networks: list[str] = Field(default_factory=list)


class ChronyConfig(BaseModel):
    general: ChronyGeneral = Field(default_factory=ChronyGeneral)
