from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.ipsec import (
    IpsecChild,
    IpsecConfig,
    IpsecConnection,
    IpsecLocal,
    IpsecPool,
    IpsecRemote,
)
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _conn_uuid(description: str) -> str:
    return make_uuid("ipsec:connection", description)


def _pool_uuid(name: str) -> str:
    return make_uuid("ipsec:pool", name)


def _child_uuid(description: str) -> str:
    return make_uuid("ipsec:child", description)


def _local_uuid(connection: str, round: int, auth: str) -> str:
    return make_uuid("ipsec:local", f"{connection}:{round}:{auth}")


def _remote_uuid(connection: str, round: int, auth: str) -> str:
    return make_uuid("ipsec:remote", f"{connection}:{round}:{auth}")


def build_ipsec(cfg: IpsecConfig) -> etree._Element | None:
    if not cfg.connections:
        return None

    el = etree.Element("Swanctl")

    _build_connections(el, cfg.connections)
    _build_locals(el, cfg.locals)
    _build_remotes(el, cfg.remotes)
    _build_children(el, cfg.children)
    _build_pools(el, cfg.pools)
    etree.SubElement(el, "VTIs")
    etree.SubElement(el, "SPDs")

    return el


def _build_connections(parent: etree._Element, connections: list[IpsecConnection]) -> None:
    cont = etree.SubElement(parent, "Connections")
    for conn in connections:
        uid = _conn_uuid(conn.description)
        el = etree.SubElement(cont, "Connection", uuid=uid)
        sub(el, "enabled", bool_val(conn.enabled))
        sub(el, "proposals", conn.proposals)
        sub(el, "unique", conn.unique)
        sub(el, "aggressive", bool_val(conn.aggressive))
        sub(el, "version", conn.version)
        sub(el, "mobike", bool_val(conn.mobike))
        if conn.local_addrs:
            sub(el, "local_addrs", conn.local_addrs)
        if conn.local_port:
            sub(el, "local_port", conn.local_port)
        if conn.remote_addrs:
            sub(el, "remote_addrs", conn.remote_addrs)
        if conn.remote_port:
            sub(el, "remote_port", conn.remote_port)
        sub(el, "encap", bool_val(conn.encap))
        if conn.reauth_time is not None:
            sub(el, "reauth_time", str(conn.reauth_time))
        if conn.rekey_time is not None:
            sub(el, "rekey_time", str(conn.rekey_time))
        if conn.dpd_delay is not None:
            sub(el, "dpd_delay", str(conn.dpd_delay))
        if conn.dpd_timeout is not None:
            sub(el, "dpd_timeout", str(conn.dpd_timeout))
        pool_uuids = ",".join(_pool_uuid(p) for p in conn.pools)
        sub(el, "pools", pool_uuids)
        sub(el, "send_certreq", bool_val(conn.send_certreq))
        if conn.send_cert:
            sub(el, "send_cert", conn.send_cert)
        if conn.keyingtries is not None:
            sub(el, "keyingtries", str(conn.keyingtries))
        sub(el, "description", conn.description)


def _build_locals(parent: etree._Element, locals_: list[IpsecLocal]) -> None:
    cont = etree.SubElement(parent, "locals")
    for local in locals_:
        uid = _local_uuid(local.connection, local.round, local.auth)
        el = etree.SubElement(cont, "local", uuid=uid)
        sub(el, "enabled", bool_val(local.enabled))
        sub(el, "connection", _conn_uuid(local.connection))
        sub(el, "round", str(local.round))
        sub(el, "auth", local.auth)
        if local.id:
            sub(el, "id", local.id)
        if local.eap_id:
            sub(el, "eap_id", local.eap_id)
        if local.certs:
            sub(el, "certs", ",".join(local.certs))
        sub(el, "description", local.description)


def _build_remotes(parent: etree._Element, remotes: list[IpsecRemote]) -> None:
    cont = etree.SubElement(parent, "remotes")
    for remote in remotes:
        uid = _remote_uuid(remote.connection, remote.round, remote.auth)
        el = etree.SubElement(cont, "remote", uuid=uid)
        sub(el, "enabled", bool_val(remote.enabled))
        sub(el, "connection", _conn_uuid(remote.connection))
        sub(el, "round", str(remote.round))
        sub(el, "auth", remote.auth)
        if remote.id:
            sub(el, "id", remote.id)
        if remote.eap_id:
            sub(el, "eap_id", remote.eap_id)
        if remote.certs:
            sub(el, "certs", ",".join(remote.certs))
        if remote.cacerts:
            sub(el, "cacerts", ",".join(remote.cacerts))
        sub(el, "description", remote.description)


def _build_children(parent: etree._Element, children: list[IpsecChild]) -> None:
    cont = etree.SubElement(parent, "children")
    for child in children:
        uid = _child_uuid(child.description)
        el = etree.SubElement(cont, "child", uuid=uid)
        sub(el, "enabled", bool_val(child.enabled))
        sub(el, "connection", _conn_uuid(child.connection))
        if child.reqid is not None:
            sub(el, "reqid", str(child.reqid))
        sub(el, "esp_proposals", child.esp_proposals)
        sub(el, "sha256_96", bool_val(child.sha256_96))
        sub(el, "start_action", child.start_action)
        sub(el, "close_action", child.close_action)
        sub(el, "dpd_action", child.dpd_action)
        sub(el, "mode", child.mode)
        sub(el, "policies", bool_val(child.policies))
        if child.local_ts:
            sub(el, "local_ts", ",".join(child.local_ts))
        if child.remote_ts:
            sub(el, "remote_ts", ",".join(child.remote_ts))
        sub(el, "rekey_time", str(child.rekey_time))
        sub(el, "description", child.description)


def _build_pools(parent: etree._Element, pools: list[IpsecPool]) -> None:
    cont = etree.SubElement(parent, "Pools")
    for pool in pools:
        uid = _pool_uuid(pool.name)
        el = etree.SubElement(cont, "Pool", uuid=uid)
        sub(el, "enabled", bool_val(pool.enabled))
        sub(el, "name", pool.name)
        sub(el, "addrs", pool.addrs)
        if pool.dns:
            sub(el, "dns", ",".join(pool.dns))
