from pydantic import BaseModel, Field


class WireguardServer(BaseModel):
    enabled: bool = True
    name: str
    privkey: str
    pubkey: str = ""
    port: str = "51820"
    mtu: int | None = None
    dns: list[str] = Field(default_factory=list)
    tunneladdress: list[str] = Field(default_factory=list)
    disableroutes: bool = False
    gateway: str = ""
    peers: list[str] = Field(default_factory=list)  # client names → resolved to UUIDs
    description: str = ""


class WireguardClient(BaseModel):
    enabled: bool = True
    name: str
    pubkey: str
    psk: str = ""
    tunneladdress: list[str] = Field(default_factory=list)
    serveraddress: str = ""
    serverport: str = "51820"
    keepalive: int | None = None
    description: str = ""


class WireguardConfig(BaseModel):
    enabled: bool = False
    servers: list[WireguardServer] = Field(default_factory=list)
    clients: list[WireguardClient] = Field(default_factory=list)
