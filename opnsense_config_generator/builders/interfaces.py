from lxml import etree

from opnsense_config_generator.models.interfaces import InterfaceConfig, InterfacesConfig
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
    # Always write mtu (empty element if not set)
    sub(el, "mtu", iface.mtu or "")

    if iface.ipaddr:
        sub(el, "ipaddr", iface.ipaddr)
    if iface.subnet:
        sub(el, "subnet", iface.subnet)
    if iface.gateway:
        sub(el, "gateway", iface.gateway)
    if iface.ipaddrv6:
        sub(el, "ipaddrv6", iface.ipaddrv6)
    if iface.subnetv6:
        sub(el, "subnetv6", iface.subnetv6)
    if iface.gatewayv6:
        sub(el, "gatewayv6", iface.gatewayv6)
    if iface.track6_interface:
        sub(el, "track6-interface", iface.track6_interface)
        sub(el, "track6-prefix-id", str(iface.track6_prefix_id))
    if iface.blockpriv:
        sub(el, "blockpriv", "1")
    if iface.blockbogons:
        sub(el, "blockbogons", "1")
    if iface.dhcphostname is not None:
        sub(el, "dhcphostname", iface.dhcphostname)
    sub(el, "media", iface.media)
    sub(el, "mediaopt", iface.mediaopt)
    if iface.spoofmac:
        sub(el, "spoofmac", iface.spoofmac)
    sub(el, "dhcp6-ia-pd-len", str(iface.dhcp6_ia_pd_len))
