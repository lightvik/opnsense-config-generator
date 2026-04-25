from pydantic import BaseModel, Field


class KeaOptionData4(BaseModel):
    routers: str = ""
    domain_name_servers: list[str] = Field(default_factory=list)
    domain_name: str = ""
    domain_search: list[str] = Field(default_factory=list)
    ntp_servers: list[str] = Field(default_factory=list)
    tftp_server_name: str = ""
    boot_file_name: str = ""


class KeaSubnet4(BaseModel):
    subnet: str
    pools: list[str] = Field(default_factory=list)
    option_data_autocollect: bool = True
    option_data: KeaOptionData4 = Field(default_factory=KeaOptionData4)
    description: str = ""


class KeaReservation4(BaseModel):
    subnet: str  # CIDR of parent subnet — resolved to UUID in builder
    hw_address: str
    ip_address: str = ""
    hostname: str = ""
    description: str = ""


class KeaDhcpv4Config(BaseModel):
    enabled: bool = False
    interfaces: list[str] = Field(default_factory=list)
    valid_lifetime: int = 4000
    fwrules: bool = True
    subnets: list[KeaSubnet4] = Field(default_factory=list)
    reservations: list[KeaReservation4] = Field(default_factory=list)


class KeaOptionData6(BaseModel):
    dns_servers: list[str] = Field(default_factory=list)
    domain_search: list[str] = Field(default_factory=list)


class KeaSubnet6(BaseModel):
    subnet: str
    interface: str = ""
    pools: list[str] = Field(default_factory=list)
    option_data: KeaOptionData6 = Field(default_factory=KeaOptionData6)
    description: str = ""


class KeaReservation6(BaseModel):
    subnet: str  # IPv6 CIDR — resolved to UUID in builder
    duid: str = ""
    hw_address: str = ""
    ip_address: str = ""
    hostname: str = ""
    description: str = ""


class KeaDhcpv6Config(BaseModel):
    enabled: bool = False
    interfaces: list[str] = Field(default_factory=list)
    valid_lifetime: int = 4000
    fwrules: bool = True
    subnets: list[KeaSubnet6] = Field(default_factory=list)
    reservations: list[KeaReservation6] = Field(default_factory=list)


class KeaCtrlAgentConfig(BaseModel):
    enabled: bool = False
    http_host: str = "127.0.0.1"
    http_port: str = "8000"


class KeaDdnsConfig(BaseModel):
    enabled: bool = False
    server_ip: str = "127.0.0.1"
    server_port: str = "53001"


class KeaConfig(BaseModel):
    dhcp4: KeaDhcpv4Config = Field(default_factory=KeaDhcpv4Config)
    dhcp6: KeaDhcpv6Config = Field(default_factory=KeaDhcpv6Config)
    ctrl_agent: KeaCtrlAgentConfig = Field(default_factory=KeaCtrlAgentConfig)
    ddns: KeaDdnsConfig = Field(default_factory=KeaDdnsConfig)
