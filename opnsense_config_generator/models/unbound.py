from pydantic import BaseModel, Field


class UnboundHostAlias(BaseModel):
    host: str
    domain: str
    descr: str = ""


class UnboundHostOverride(BaseModel):
    host: str
    domain: str
    ip: str
    descr: str = ""
    aliases: list[str] = Field(default_factory=list)
    rr: str = ""
    mxprio: str = ""
    ttl: str = ""
    txtdata: str = ""
    addptr: bool = False
    alias: list[UnboundHostAlias] = Field(default_factory=list)


class UnboundDomainOverride(BaseModel):
    domain: str
    ip: str
    descr: str = ""


class UnboundAcl(BaseModel):
    aclname: str
    aclaction: str = "allow"
    description: str = ""
    networks: list[str] = Field(default_factory=list)


class UnboundDot(BaseModel):
    server: str
    port: str = "853"
    verify: str = ""


class UnboundConfig(BaseModel):
    enable: bool = True
    dnssec: bool = True
    forwarding: bool = False
    forward_tls_upstream: bool = False
    active_interface: str = ""
    outgoing_interface: str = ""
    hosts: list[UnboundHostOverride] = Field(default_factory=list)
    domainoverrides: list[UnboundDomainOverride] = Field(default_factory=list)
    custom_options: str = ""
    forward_servers: list[str] = Field(default_factory=list)
    cache_max_ttl: int = 86400
    cache_min_ttl: int = 0
    hide_identity: bool = True
    hide_version: bool = True
    log_queries: bool = False
    prefetch: bool = False
    prefetch_key: bool = False
    dns64: bool = False
    port: str = ""
    stats: bool = False
    dns64prefix: str = ""
    noarecords: bool = False
    regdhcp: bool = False
    regdhcpdomain: str = ""
    regdhcpstatic: bool = False
    noreglladdr6: bool = False
    txtsupport: bool = False
    safesearch: bool = False
    local_zone_type: str = ""
    enable_wpad: bool = False
    dnssecstripped: bool = False
    belownxdomain: bool = False
    aggressivensec: bool = False
    serveexpired: bool = False
    serveexpiredttl: int | None = None
    serveexpiredttlreset: bool = False
    serveexpiredclienttimeout: int | None = None
    qnameminstrict: bool = False
    extendedstatistics: bool = False
    logverbosity: str = ""
    logqueries: bool = False
    logreplies: bool = False
    logtagqueryreply: bool = False
    loglocal: bool = False
    privatedomain: list[str] = Field(default_factory=list)
    privateaddress: list[str] = Field(default_factory=list)
    insecuredomain: list[str] = Field(default_factory=list)
    msgcachesize: int | None = None
    rrsetcachesize: int | None = None
    outgoingnumtcp: int | None = None
    incomingnumtcp: int | None = None
    numqueriesperthread: int | None = None
    jostle_timeout: int | None = None
    acls: list[UnboundAcl] = Field(default_factory=list)
    dots: list[UnboundDot] = Field(default_factory=list)
