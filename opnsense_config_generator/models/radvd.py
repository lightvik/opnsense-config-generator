from typing import Literal

from pydantic import BaseModel, Field

RadvdMode = Literal["router", "unmanaged", "managed", "assist", "stateless"]
RadvdPreference = Literal["low", "medium", "high"]
RadvdBoolOpt = Literal["on", "off"]


class RadvdEntry(BaseModel):
    enabled: bool = True
    interface: str
    base6_interface: str = ""
    mode: RadvdMode = "stateless"
    deprecate_prefix: RadvdBoolOpt | None = None
    remove_adv_on_exit: RadvdBoolOpt | None = None
    remove_route: RadvdBoolOpt | None = None
    routes: list[str] = Field(default_factory=list)
    rdnss: list[str] = Field(default_factory=list)
    dnssl: list[str] = Field(default_factory=list)
    dns: bool = True
    min_rtr_adv_interval: int = 200
    max_rtr_adv_interval: int = 600
    adv_dnssl_lifetime: int | None = None
    adv_default_lifetime: int | None = None
    adv_link_mtu: int | None = None
    adv_preferred_lifetime: int | None = None
    adv_ra_src_address: str = ""
    adv_rdnss_lifetime: int | None = None
    adv_route_lifetime: int | None = None
    adv_valid_lifetime: int | None = None
    adv_default_preference: RadvdPreference = "medium"
    nat64prefix: str = ""
    adv_cur_hop_limit: int = 64


class RadvdConfig(BaseModel):
    entries: list[RadvdEntry] = Field(default_factory=list)
