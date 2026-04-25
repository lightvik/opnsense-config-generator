from typing import Literal

from pydantic import BaseModel, Field

BindDnssecValidation = Literal["no", "auto"]
BindRndcAlgo = Literal[
    "hmac-sha512", "hmac-sha384", "hmac-sha256",
    "hmac-sha224", "hmac-sha1", "hmac-md5",
]
BindLogLevel = Literal["crit", "error", "warn", "notice", "info", "debug", "dynamic"]
BindDomainType = Literal["primary", "secondary", "forward"]
BindRecordType = Literal[
    "A", "AAAA", "CAA", "CNAME", "DNAME", "DNSKEY", "DS",
    "MX", "NS", "PTR", "RP", "RRSIG", "SRV", "SSHFP", "TLSA", "TXT",
]


class BindGeneral(BaseModel):
    enabled: bool = False
    disablev6: bool = False
    enablerpz: bool = True
    listenv4: list[str] = Field(default_factory=lambda: ["0.0.0.0"])
    listenv6: list[str] = Field(default_factory=lambda: ["::"])
    port: int = 53530
    forwarders: list[str] = Field(default_factory=list)
    filteraaaav4: bool = False
    filteraaaav6: bool = False
    filteraaaaacl: list[str] = Field(default_factory=list)
    logsize: int = 5
    general_log_level: BindLogLevel = "info"
    maxcachesize: int = 80
    recursion: list[str] = Field(default_factory=list)
    allowtransfer: list[str] = Field(default_factory=list)
    allowquery: list[str] = Field(default_factory=list)
    dnssecvalidation: BindDnssecValidation = "no"
    hidehostname: bool = False
    hideversion: bool = False
    disableprefetch: bool = False
    enableratelimiting: bool = False
    ratelimitcount: int | None = None
    ratelimitexcept: list[str] = Field(default_factory=lambda: ["0.0.0.0", "::"])
    rndcalgo: BindRndcAlgo = "hmac-sha256"
    rndcsecret: str = "VxtIzJevSQXqnr7h2qerrcwjnZlMWSGGFBndKeNIDfw="
    querysource: str = ""
    querysourcev6: str = ""
    transfersource: str = ""
    transfersourcev6: str = ""


class BindAcl(BaseModel):
    name: str
    enabled: bool = True
    networks: list[str]


class BindDomain(BaseModel):
    enabled: bool = True
    type: BindDomainType = "primary"
    domainname: str
    primaryip: list[str] = Field(default_factory=list)
    forwardserver: list[str] = Field(default_factory=list)
    allowtransfer: list[str] = Field(default_factory=list)
    allowquery: list[str] = Field(default_factory=list)
    allowrndctransfer: bool = False
    allowrndcupdate: bool = True
    serial: str = ""
    ttl: int = 86400
    refresh: int = 21600
    retry: int = 3600
    expire: int = 3542400
    negative: int = 3600
    mailadmin: str = "mail.opnsense.localdomain"
    dnsserver: str = "opnsense.localdomain"
    transferkeyalgo: str = ""
    transferkeyname: str = ""
    transferkey: str = ""
    allownotifysecondary: list[str] = Field(default_factory=list)


class BindRecord(BaseModel):
    enabled: bool = True
    domain: str
    name: str = ""
    type: BindRecordType = "A"
    value: str


class BindDnsbl(BaseModel):
    enabled: bool = False
    type: list[str] = Field(default_factory=list)
    whitelists: list[str] = Field(default_factory=list)
    forcesafegoogle: bool = False
    forcesafeduckduckgo: bool = False
    forcesafeyoutube: bool = False
    forcestrictbing: bool = False


class BindConfig(BaseModel):
    general: BindGeneral = Field(default_factory=BindGeneral)
    acls: list[BindAcl] = Field(default_factory=list)
    domains: list[BindDomain] = Field(default_factory=list)
    records: list[BindRecord] = Field(default_factory=list)
    dnsbl: BindDnsbl = Field(default_factory=BindDnsbl)
