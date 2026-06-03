from pydantic import BaseModel, Field


class DnsmasqDhcpRange(BaseModel):
    interface: str
    start_addr: str
    end_addr: str
    constructor: str = ""
    ra_mode: str = ""


class DnsmasqDhcp(BaseModel):
    enable_ra: bool = False


class DnsmasqHost(BaseModel):
    host: str
    domain: str
    ip: str
    descr: str = ""
    mac: str = ""


class DnsmasqDomainOverride(BaseModel):
    domain: str
    ip: str
    descr: str = ""


class DnsmasqDhcpOption(BaseModel):
    tag: str = ""
    number: str
    value: str = ""


class DnsmasqConfig(BaseModel):
    enable: bool = False
    port: str = "53053"
    interface: str = "lan"
    dhcp: DnsmasqDhcp = Field(default_factory=DnsmasqDhcp)
    dhcp_ranges: list[DnsmasqDhcpRange] = Field(default_factory=list)
    regdhcp: bool = False
    regdhcpstatic: bool = False
    strict_order: bool = False
    dhcpfirst: bool = False
    domain_needed: bool = False
    no_private_reverse: bool = False
    no_resolv: bool = False
    log_queries: bool = False
    no_hosts: bool = False
    strictbind: bool = False
    dnssec: bool = False
    regdhcpdomain: str = ""
    dns_forward_max: int | None = None
    cache_size: int | None = None
    local_ttl: int | None = None
    add_mac: bool = False
    hosts: list[DnsmasqHost] = Field(default_factory=list)
    domainoverrides: list[DnsmasqDomainOverride] = Field(default_factory=list)
    dhcp_options: list[DnsmasqDhcpOption] = Field(default_factory=list)
