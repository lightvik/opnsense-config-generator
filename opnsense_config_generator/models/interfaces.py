from typing import Literal

from pydantic import BaseModel, Field


class InterfaceConfig(BaseModel):
    enable: bool = True
    descr: str = ""
    # Physical interface name (e.g. vtnet0, em0, igb0)
    if_name: str = Field(alias="if")
    # IPv4
    ipaddr: str = ""
    subnet: str = ""
    gateway: str = ""
    # IPv6
    ipaddrv6: str = ""
    subnetv6: str = ""
    gatewayv6: str = ""
    # track6 (delegated prefix from WAN)
    track6_interface: str = Field(default="", alias="track6-interface")
    track6_prefix_id: int = Field(default=0, alias="track6-prefix-id")
    # DHCP/misc
    dhcphostname: str = ""
    mtu: str = ""
    media: str = ""
    mediaopt: str = ""
    blockpriv: bool = False
    blockbogons: bool = False
    spoofmac: str = ""
    dhcp6_ia_pd_len: int = Field(default=0, alias="dhcp6-ia-pd-len")
    # VLAN parent + tag (for VLAN interfaces auto-created in assignments)
    vlanif: str = ""

    model_config = {"populate_by_name": True}


class InterfacesConfig(BaseModel):
    # Key = interface assignment name (wan, lan, opt1, …)
    interfaces: dict[str, InterfaceConfig] = Field(default_factory=dict)
