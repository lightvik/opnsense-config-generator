from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.wireguard import WireguardConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _server_uuid(name: str) -> str:
    return make_uuid("wireguard:server", name)


def _client_uuid(name: str) -> str:
    return make_uuid("wireguard:client", name)


def build_wireguard(cfg: WireguardConfig) -> etree._Element | None:
    if not cfg.enabled and not cfg.servers and not cfg.clients:
        return None

    el = etree.Element("wireguard")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.enabled))

    server_el = etree.SubElement(el, "server")
    servers_el = etree.SubElement(server_el, "servers")
    for i, srv in enumerate(cfg.servers):
        uid = _server_uuid(srv.name)
        s = etree.SubElement(servers_el, "server", uuid=uid)
        sub(s, "enabled", bool_val(srv.enabled))
        sub(s, "name", srv.name)
        sub(s, "instance", str(i))
        if srv.pubkey:
            sub(s, "pubkey", srv.pubkey)
        sub(s, "privkey", srv.privkey)
        sub(s, "port", srv.port)
        if srv.mtu is not None:
            sub(s, "mtu", str(srv.mtu))
        if srv.dns:
            sub(s, "dns", ",".join(srv.dns))
        if srv.tunneladdress:
            sub(s, "tunneladdress", ",".join(srv.tunneladdress))
        sub(s, "disableroutes", bool_val(srv.disableroutes))
        if srv.gateway:
            sub(s, "gateway", srv.gateway)
        peer_uuids = ",".join(_client_uuid(p) for p in srv.peers)
        sub(s, "peers", peer_uuids)
        sub(s, "debug", "0")

    client_el = etree.SubElement(el, "client")
    clients_el = etree.SubElement(client_el, "clients")
    for cli in cfg.clients:
        uid = _client_uuid(cli.name)
        c = etree.SubElement(clients_el, "client", uuid=uid)
        sub(c, "enabled", bool_val(cli.enabled))
        sub(c, "name", cli.name)
        sub(c, "pubkey", cli.pubkey)
        if cli.psk:
            sub(c, "psk", cli.psk)
        if cli.tunneladdress:
            sub(c, "tunneladdress", ",".join(cli.tunneladdress))
        if cli.serveraddress:
            sub(c, "serveraddress", cli.serveraddress)
        sub(c, "serverport", cli.serverport)
        if cli.keepalive is not None:
            sub(c, "keepalive", str(cli.keepalive))

    return el
