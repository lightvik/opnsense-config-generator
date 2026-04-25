from typing import Literal

from pydantic import BaseModel, Field

IpsecAuth = Literal["psk", "pubkey", "eap-tls", "eap-mschapv2", "xauth-pam", "eap-radius"]
IpsecVersion = Literal["0", "1", "2"]  # 0=IKEv1+v2, 1=IKEv1, 2=IKEv2


class IpsecConnection(BaseModel):
    enabled: bool = True
    description: str
    proposals: str = "default"
    unique: Literal["no", "never", "keep", "replace"] = "no"
    aggressive: bool = False
    version: IpsecVersion = "2"
    mobike: bool = True
    local_addrs: str = ""
    remote_addrs: str = ""
    local_port: str = ""
    remote_port: str = ""
    encap: bool = False
    reauth_time: int | None = None
    rekey_time: int | None = None
    dpd_delay: int | None = None
    dpd_timeout: int | None = None
    send_certreq: bool = True
    send_cert: str = ""
    keyingtries: int | None = None
    pools: list[str] = Field(default_factory=list)  # pool names → resolved to UUIDs


class IpsecLocal(BaseModel):
    enabled: bool = True
    connection: str  # connection description → resolved to UUID
    round: int = 0
    auth: IpsecAuth = "psk"
    id: str = ""
    eap_id: str = ""
    certs: list[str] = Field(default_factory=list)
    description: str = ""


class IpsecRemote(BaseModel):
    enabled: bool = True
    connection: str  # connection description → resolved to UUID
    round: int = 0
    auth: IpsecAuth = "psk"
    id: str = ""
    eap_id: str = ""
    certs: list[str] = Field(default_factory=list)
    cacerts: list[str] = Field(default_factory=list)
    description: str = ""


class IpsecChild(BaseModel):
    enabled: bool = True
    connection: str  # connection description → resolved to UUID
    description: str = ""
    esp_proposals: str = "default"
    sha256_96: bool = False
    start_action: Literal["none", "trap|start", "route", "start", "trap"] = "start"
    close_action: Literal["none", "trap", "start"] = "none"
    dpd_action: Literal["clear", "trap", "start"] = "clear"
    mode: Literal["tunnel", "transport", "pass", "drop"] = "tunnel"
    policies: bool = True
    local_ts: list[str] = Field(default_factory=list)
    remote_ts: list[str] = Field(default_factory=list)
    rekey_time: int = 3600
    reqid: int | None = None


class IpsecPool(BaseModel):
    enabled: bool = True
    name: str
    addrs: str  # CIDR network for IP pool
    dns: list[str] = Field(default_factory=list)


class IpsecConfig(BaseModel):
    connections: list[IpsecConnection] = Field(default_factory=list)
    locals: list[IpsecLocal] = Field(default_factory=list)
    remotes: list[IpsecRemote] = Field(default_factory=list)
    children: list[IpsecChild] = Field(default_factory=list)
    pools: list[IpsecPool] = Field(default_factory=list)
