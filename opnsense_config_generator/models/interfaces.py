from typing import Literal

from pydantic import BaseModel, Field


class WirelessConfig(BaseModel):
    mode: Literal["bss", "adhoc", "hostap"] = "bss"
    ssid: str = ""
    channel: str = "0"
    authmode: str = ""
    txpower: str = ""
    standard: str = ""
    puremode: str = ""
    wpa_mode: str = Field(default="", alias="wpa_mode")
    wpa_key_mgmt: str = Field(default="", alias="wpa_key_mgmt")
    wpa_pairwise: str = Field(default="", alias="wpa_pairwise")
    passphrase: str = ""
    wpa_group_rekey: str = ""
    wpa_gmk_rekey: str = ""
    wpa_strict_rekey: bool = False
    hidessid: bool = False

    model_config = {"populate_by_name": True}


class InterfaceConfig(BaseModel):
    enable: bool = True
    descr: str = ""
    if_name: str = Field(alias="if")
    ipaddr: str = ""
    subnet: str = ""
    gateway: str = ""
    ipaddrv6: str = ""
    subnetv6: str = ""
    gatewayv6: str = ""
    track6_interface: str = Field(default="", alias="track6-interface")
    track6_prefix_id: int = Field(default=0, alias="track6-prefix-id")
    dhcphostname: str = ""
    mtu: str = ""
    media: str = ""
    mediaopt: str = ""
    blockpriv: bool = False
    blockbogons: bool = False
    spoofmac: str = ""
    dhcp6_ia_pd_len: int = Field(default=0, alias="dhcp6-ia-pd-len")
    vlanif: str = ""
    lock: bool = False
    promisc: bool = False
    mss: str = ""
    gateway_interface: bool = False
    dhcprejectfrom: str = ""
    dhcpvlanprio: str = ""
    dhcphonourmtu: bool = False
    alias_address: str = Field(default="", alias="alias-address")
    alias_subnet: str = Field(default="", alias="alias-subnet")
    gateway_6rd: str = Field(default="", alias="gateway-6rd")
    prefix_6rd: str = Field(default="", alias="prefix-6rd")
    prefix_6rd_v4addr: str = Field(default="", alias="prefix-6rd-v4addr")
    prefix_6rd_v4plen: str = Field(default="", alias="prefix-6rd-v4plen")
    dhcp6_ifid: str = ""
    dhcp6_rapid_commit: bool = False
    dhcp6prefixonly: bool = False
    dhcp6_ia_pd_send_hint: bool = Field(default=False, alias="dhcp6-ia-pd-send-hint")
    disableipv6: bool = False
    wireless: WirelessConfig | None = None
    disablechecksumoffloading: bool = False
    disablesegmentationoffloading: bool = False
    disablelargereceiveoffloading: bool = False
    disablevlanoffloading: bool = False

    model_config = {"populate_by_name": True}


class InterfacesConfig(BaseModel):
    interfaces: dict[str, InterfaceConfig] = Field(default_factory=dict)
