from pydantic import BaseModel, Field


class UnboundHostOverride(BaseModel):
    host: str
    domain: str
    ip: str
    descr: str = ""
    aliases: list[str] = Field(default_factory=list)


class UnboundDomainOverride(BaseModel):
    domain: str
    ip: str
    descr: str = ""


class UnboundConfig(BaseModel):
    enable: bool = True
    dnssec: bool = True
    forwarding: bool = False
    forward_tls_upstream: bool = False
    # space-separated interfaces to listen on (empty = all)
    active_interface: str = ""
    outgoing_interface: str = ""
    # hosts overrides
    hosts: list[UnboundHostOverride] = Field(default_factory=list)
    # domain overrides (forward specific domains)
    domainoverrides: list[UnboundDomainOverride] = Field(default_factory=list)
    # custom options (raw unbound.conf lines)
    custom_options: str = ""
    # query forwarding servers (used when forwarding=true)
    forward_servers: list[str] = Field(default_factory=list)
    cache_max_ttl: int = 86400
    cache_min_ttl: int = 0
    hide_identity: bool = True
    hide_version: bool = True
    log_queries: bool = False
    prefetch: bool = False
    prefetch_key: bool = False
    dns64: bool = False
