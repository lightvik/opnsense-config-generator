from pydantic import BaseModel, Field


class DnsmasqDhcpRange(BaseModel):
    interface: str
    start_addr: str
    end_addr: str
    constructor: str = ""  # IPv6: parent interface для prefix delegation
    ra_mode: str = ""      # slaac | ra-only | ra-stateless | ra-names | ra-advrouter


class DnsmasqDhcp(BaseModel):
    enable_ra: bool = False  # IPv6 Router Advertisements


class DnsmasqConfig(BaseModel):
    enable: bool = False
    port: str = "53053"   # Unbound занимает 53; dnsmasq слушает на этом порту
    interface: str = "lan"
    dhcp: DnsmasqDhcp = Field(default_factory=DnsmasqDhcp)
    dhcp_ranges: list[DnsmasqDhcpRange] = Field(default_factory=list)
    regdhcp: bool = False        # регистрировать DHCP-аренды в DNS
    regdhcpstatic: bool = False  # регистрировать статические резервации в DNS
    strict_order: bool = False   # опрашивать upstream DNS в заданном порядке
