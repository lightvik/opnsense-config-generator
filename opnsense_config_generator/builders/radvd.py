from lxml import etree

from opnsense_config_generator.builders.base import append_if, bool_val
from opnsense_config_generator.models.radvd import RadvdEntry, RadvdConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _entry_uuid(interface: str) -> str:
    return make_uuid("radvd:entry", interface)


def _build_entry(parent: etree._Element, entry: RadvdEntry) -> None:
    el = etree.SubElement(parent, "entries")
    el.set("uuid", _entry_uuid(entry.interface))

    sub(el, "enabled", bool_val(entry.enabled))
    sub(el, "interface", entry.interface)
    append_if(el, "Base6Interface", entry.base6_interface or None)
    sub(el, "mode", entry.mode)
    append_if(el, "DeprecatePrefix", entry.deprecate_prefix)
    append_if(el, "RemoveAdvOnExit", entry.remove_adv_on_exit)
    append_if(el, "RemoveRoute", entry.remove_route)
    if entry.routes:
        sub(el, "routes", ",".join(entry.routes))
    if entry.rdnss:
        sub(el, "RDNSS", ",".join(entry.rdnss))
    if entry.dnssl:
        sub(el, "DNSSL", ",".join(entry.dnssl))
    sub(el, "dns", bool_val(entry.dns))
    sub(el, "MinRtrAdvInterval", str(entry.min_rtr_adv_interval))
    sub(el, "MaxRtrAdvInterval", str(entry.max_rtr_adv_interval))
    append_if(el, "AdvDNSSLLifetime", entry.adv_dnssl_lifetime)
    append_if(el, "AdvDefaultLifetime", entry.adv_default_lifetime)
    append_if(el, "AdvLinkMTU", entry.adv_link_mtu)
    append_if(el, "AdvPreferredLifetime", entry.adv_preferred_lifetime)
    append_if(el, "AdvRASrcAddress", entry.adv_ra_src_address or None)
    append_if(el, "AdvRDNSSLifetime", entry.adv_rdnss_lifetime)
    append_if(el, "AdvRouteLifetime", entry.adv_route_lifetime)
    append_if(el, "AdvValidLifetime", entry.adv_valid_lifetime)
    sub(el, "AdvDefaultPreference", entry.adv_default_preference)
    append_if(el, "nat64prefix", entry.nat64prefix or None)
    sub(el, "AdvCurHopLimit", str(entry.adv_cur_hop_limit))


def build_radvd(cfg: RadvdConfig) -> etree._Element | None:
    if not cfg.entries:
        return None

    el = etree.Element("radvd")
    for entry in cfg.entries:
        _build_entry(el, entry)
    return el
