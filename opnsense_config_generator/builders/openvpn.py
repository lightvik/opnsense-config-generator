from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.openvpn import (
    OpenVpnConfig,
    OpenVpnInstance,
    OpenVpnStaticKey,
)
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _instance_uuid(vpnid: int) -> str:
    return make_uuid("openvpn:instance", str(vpnid))


def _static_key_uuid(description: str) -> str:
    return make_uuid("openvpn:statickey", description)


def build_openvpn(cfg: OpenVpnConfig) -> etree._Element | None:
    if not cfg.instances and not cfg.static_keys:
        return None

    el = etree.Element("OpenVPN")

    _build_instances(el, cfg.instances)
    _build_static_keys(el, cfg.static_keys)
    etree.SubElement(el, "Overwrites")

    return el


def _build_instances(parent: etree._Element, instances: list[OpenVpnInstance]) -> None:
    cont = etree.SubElement(parent, "Instances")
    for i, inst in enumerate(instances):
        vpnid = i + 1
        uid = _instance_uuid(vpnid)
        el = etree.SubElement(cont, "Instance", uuid=uid)

        sub(el, "vpnid", str(vpnid))
        sub(el, "enabled", bool_val(inst.enabled))
        sub(el, "dev_type", inst.dev_type)
        sub(el, "verb", inst.verb)
        sub(el, "proto", inst.proto)
        if inst.port:
            sub(el, "port", inst.port)
        if inst.local:
            sub(el, "local", inst.local)
        if inst.remote:
            sub(el, "remote", inst.remote)
        sub(el, "topology", inst.topology)
        sub(el, "role", inst.role)
        if inst.server:
            sub(el, "server", inst.server)
        if inst.server_ipv6:
            sub(el, "server_ipv6", inst.server_ipv6)
        if inst.ca:
            sub(el, "ca", inst.ca)
        if inst.cert:
            sub(el, "cert", inst.cert)
        if inst.tls_key:
            sub(el, "tls_key", inst.tls_key)
        if inst.cert_depth:
            sub(el, "cert_depth", inst.cert_depth)
        sub(el, "remote_cert_tls", bool_val(inst.remote_cert_tls))
        sub(el, "verify_client_cert", inst.verify_client_cert)
        if inst.auth:
            sub(el, "auth", inst.auth)
        if inst.data_ciphers:
            sub(el, "data-ciphers", ",".join(inst.data_ciphers))
        if inst.data_ciphers_fallback:
            sub(el, "data-ciphers-fallback", inst.data_ciphers_fallback)
        if inst.push_route:
            sub(el, "push_route", ",".join(inst.push_route))
        if inst.route:
            sub(el, "route", ",".join(inst.route))
        if inst.dns_servers:
            sub(el, "dns_servers", ",".join(inst.dns_servers))
        if inst.ntp_servers:
            sub(el, "ntp_servers", ",".join(inst.ntp_servers))
        if inst.redirect_gateway:
            sub(el, "redirect_gateway", ",".join(inst.redirect_gateway))
        if inst.various_flags:
            sub(el, "various_flags", ",".join(inst.various_flags))
        if inst.keepalive_interval is not None:
            sub(el, "keepalive_interval", str(inst.keepalive_interval))
        if inst.keepalive_timeout is not None:
            sub(el, "keepalive_timeout", str(inst.keepalive_timeout))
        if inst.maxclients is not None:
            sub(el, "maxclients", str(inst.maxclients))
        sub(el, "username_as_common_name", bool_val(inst.username_as_common_name))
        if inst.username:
            sub(el, "username", inst.username)
        if inst.password:
            sub(el, "password", inst.password)
        sub(el, "description", inst.description)


def _build_static_keys(parent: etree._Element, keys: list[OpenVpnStaticKey]) -> None:
    cont = etree.SubElement(parent, "StaticKeys")
    for key in keys:
        uid = _static_key_uuid(key.description)
        el = etree.SubElement(cont, "StaticKey", uuid=uid)
        sub(el, "mode", key.mode)
        sub(el, "key", key.key)
        sub(el, "description", key.description)
