from lxml import etree

from opnsense_config_generator.models.interfaces import InterfaceConfig, InterfacesConfig, WirelessConfig
from opnsense_config_generator.xml_utils import sub


def build_interfaces(cfg: InterfacesConfig) -> etree._Element:
    interfaces = etree.Element("interfaces")
    for name, iface in cfg.interfaces.items():
        _build_interface(interfaces, name, iface)
    return interfaces


def _build_interface(parent: etree._Element, name: str, iface: InterfaceConfig) -> None:
    el = etree.SubElement(parent, name)

    if iface.enable:
        sub(el, "enable", "1")
    if iface.descr:
        sub(el, "descr", iface.descr)
    sub(el, "if", iface.if_name)
    sub(el, "mtu", iface.mtu or "")

    if iface.lock:
        sub(el, "lock")
    if iface.promisc:
        sub(el, "promisc")
    if iface.mss:
        sub(el, "mss", iface.mss)
    if iface.gateway_interface:
        sub(el, "gateway_interface")
    if iface.spoofmac:
        sub(el, "spoofmac", iface.spoofmac)

    if iface.ipaddr:
        sub(el, "ipaddr", iface.ipaddr)
    if iface.subnet:
        sub(el, "subnet", iface.subnet)
    if iface.gateway:
        sub(el, "gateway", iface.gateway)
    if iface.alias_address:
        sub(el, "alias-address", iface.alias_address)
    if iface.alias_subnet:
        sub(el, "alias-subnet", iface.alias_subnet)
    if iface.dhcphostname is not None:
        sub(el, "dhcphostname", iface.dhcphostname)
    if iface.dhcprejectfrom:
        sub(el, "dhcprejectfrom", iface.dhcprejectfrom)
    if iface.dhcpvlanprio:
        sub(el, "dhcpvlanprio", iface.dhcpvlanprio)
    if iface.dhcphonourmtu:
        sub(el, "dhcphonourmtu")

    if iface.ipaddrv6:
        sub(el, "ipaddrv6", iface.ipaddrv6)
    if iface.subnetv6:
        sub(el, "subnetv6", iface.subnetv6)
    if iface.gatewayv6:
        sub(el, "gatewayv6", iface.gatewayv6)
    if iface.track6_interface:
        sub(el, "track6-interface", iface.track6_interface)
        sub(el, "track6-prefix-id", str(iface.track6_prefix_id))
    if iface.gateway_6rd:
        sub(el, "gateway-6rd", iface.gateway_6rd)
        if iface.prefix_6rd:
            sub(el, "prefix-6rd", iface.prefix_6rd)
        if iface.prefix_6rd_v4addr:
            sub(el, "prefix-6rd-v4addr", iface.prefix_6rd_v4addr)
        if iface.prefix_6rd_v4plen:
            sub(el, "prefix-6rd-v4plen", iface.prefix_6rd_v4plen)
    if iface.disableipv6:
        sub(el, "disableipv6")
    if iface.dhcp6_ifid:
        sub(el, "dhcp6-ifid", iface.dhcp6_ifid)
    if iface.dhcp6_rapid_commit:
        sub(el, "dhcp6_rapid_commit")
    if iface.dhcp6prefixonly:
        sub(el, "dhcp6prefixonly")
    if iface.dhcp6_ia_pd_send_hint:
        sub(el, "dhcp6-ia-pd-send-hint")
    sub(el, "dhcp6-ia-pd-len", str(iface.dhcp6_ia_pd_len))

    if iface.blockpriv:
        sub(el, "blockpriv", "1")
    if iface.blockbogons:
        sub(el, "blockbogons", "1")

    sub(el, "media", iface.media)
    sub(el, "mediaopt", iface.mediaopt)

    if iface.disablechecksumoffloading:
        sub(el, "disablechecksumoffloading")
    if iface.disablesegmentationoffloading:
        sub(el, "disablesegmentationoffloading")
    if iface.disablelargereceiveoffloading:
        sub(el, "disablelargereceiveoffloading")
    if iface.disablevlanoffloading:
        sub(el, "disablevlanoffloading")

    if iface.wireless is not None:
        _build_wireless(el, iface.wireless)


def _build_wireless(parent: etree._Element, w: WirelessConfig) -> None:
    wl = etree.SubElement(parent, "wireless")
    sub(wl, "mode", w.mode)
    if w.ssid:
        sub(wl, "ssid", w.ssid)
    sub(wl, "channel", w.channel)
    if w.authmode:
        sub(wl, "authmode", w.authmode)
    if w.standard:
        sub(wl, "standard", w.standard)
    if w.puremode:
        sub(wl, "puremode", w.puremode)
    if w.txpower:
        sub(wl, "txpower", w.txpower)
    if w.wpa_mode:
        sub(wl, "wpa_mode", w.wpa_mode)
    if w.wpa_key_mgmt:
        sub(wl, "wpa_key_mgmt", w.wpa_key_mgmt)
    if w.wpa_pairwise:
        sub(wl, "wpa_pairwise", w.wpa_pairwise)
    if w.passphrase:
        sub(wl, "passphrase", w.passphrase)
    if w.wpa_group_rekey:
        sub(wl, "wpa_group_rekey", w.wpa_group_rekey)
    if w.wpa_gmk_rekey:
        sub(wl, "wpa_gmk_rekey", w.wpa_gmk_rekey)
    if w.wpa_strict_rekey:
        sub(wl, "wpa_strict_rekey")
    if w.hidessid:
        sub(wl, "hidessid")
