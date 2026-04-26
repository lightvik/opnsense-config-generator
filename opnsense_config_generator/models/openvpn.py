from typing import Literal

from pydantic import BaseModel, Field

OpenVpnProto = Literal["udp", "udp4", "udp6", "tcp", "tcp4", "tcp6"]
OpenVpnDevType = Literal["tun", "tap", "ovpn"]
OpenVpnRole = Literal["server", "client"]
OpenVpnTopology = Literal["subnet", "net30", "p2p"]


class OpenVpnStaticKey(BaseModel):
    mode: Literal["auth", "crypt"] = "crypt"
    key: str
    description: str


class OpenVpnInstance(BaseModel):
    enabled: bool = True
    description: str = ""
    role: OpenVpnRole = "server"
    dev_type: OpenVpnDevType = "tun"
    proto: OpenVpnProto = "udp"
    port: str = "1194"
    local: str = ""  # local bind address (empty = all interfaces)
    remote: str = ""  # remote server address (client role)
    server: str = ""  # server pool CIDR (e.g. 10.8.0.0/24)
    server_ipv6: str = ""
    topology: OpenVpnTopology = "subnet"
    ca: str = ""  # caref
    cert: str = ""  # certref
    tls_key: str = ""  # uuid of StaticKey
    verify_client_cert: Literal["require", "none"] = "require"
    remote_cert_tls: bool = False
    cert_depth: str = ""
    auth: str = ""
    data_ciphers: list[str] = Field(default_factory=list)
    data_ciphers_fallback: str = ""
    push_route: list[str] = Field(default_factory=list)
    route: list[str] = Field(default_factory=list)
    dns_servers: list[str] = Field(default_factory=list)
    ntp_servers: list[str] = Field(default_factory=list)
    redirect_gateway: list[str] = Field(default_factory=list)
    various_flags: list[str] = Field(default_factory=list)
    keepalive_interval: int | None = None
    keepalive_timeout: int | None = None
    maxclients: int | None = None
    verb: str = "3"
    username_as_common_name: bool = False
    username: str = ""
    password: str = ""


class OpenVpnConfig(BaseModel):
    instances: list[OpenVpnInstance] = Field(default_factory=list)
    static_keys: list[OpenVpnStaticKey] = Field(default_factory=list)
