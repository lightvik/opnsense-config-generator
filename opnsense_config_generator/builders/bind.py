from lxml import etree

from opnsense_config_generator.builders.base import append_if, bool_val
from opnsense_config_generator.models.bind import BindAcl, BindConfig, BindDomain, BindRecord
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _acl_uuid(name: str) -> str:
    return make_uuid("bind:acl", name)


def _domain_uuid(name: str) -> str:
    return make_uuid("bind:domain", name)


def _resolve_acl_uuids(names: list[str]) -> str:
    return ",".join(_acl_uuid(n) for n in names)


def _build_acl(parent: etree._Element, acl: BindAcl) -> None:
    el = etree.SubElement(parent, "acl", uuid=_acl_uuid(acl.name))
    sub(el, "enabled", bool_val(acl.enabled))
    sub(el, "name", acl.name)
    sub(el, "networks", ",".join(acl.networks))


def _build_domain(parent: etree._Element, domain: BindDomain) -> None:
    el = etree.SubElement(parent, "domain", uuid=_domain_uuid(domain.domainname))
    sub(el, "enabled", bool_val(domain.enabled))
    sub(el, "type", domain.type)
    sub(el, "domainname", domain.domainname)
    if domain.primaryip:
        sub(el, "primaryip", ",".join(domain.primaryip))
    if domain.forwardserver:
        sub(el, "forwardserver", ",".join(domain.forwardserver))
    if domain.allowtransfer:
        sub(el, "allowtransfer", _resolve_acl_uuids(domain.allowtransfer))
    sub(el, "allowrndctransfer", bool_val(domain.allowrndctransfer))
    if domain.allowquery:
        sub(el, "allowquery", _resolve_acl_uuids(domain.allowquery))
    sub(el, "allowrndcupdate", bool_val(domain.allowrndcupdate))
    append_if(el, "serial", domain.serial or None)
    sub(el, "ttl", str(domain.ttl))
    sub(el, "refresh", str(domain.refresh))
    sub(el, "retry", str(domain.retry))
    sub(el, "expire", str(domain.expire))
    sub(el, "negative", str(domain.negative))
    sub(el, "mailadmin", domain.mailadmin)
    sub(el, "dnsserver", domain.dnsserver)
    append_if(el, "transferkeyalgo", domain.transferkeyalgo or None)
    append_if(el, "transferkeyname", domain.transferkeyname or None)
    append_if(el, "transferkey", domain.transferkey or None)
    if domain.allownotifysecondary:
        sub(el, "allownotifysecondary", ",".join(domain.allownotifysecondary))


def _build_record(parent: etree._Element, record: BindRecord) -> None:
    record_key = f"{record.domain}:{record.name}:{record.type}:{record.value}"
    el = etree.SubElement(parent, "record", uuid=make_uuid("bind:record", record_key))
    sub(el, "enabled", bool_val(record.enabled))
    sub(el, "domain", _domain_uuid(record.domain))
    sub(el, "name", record.name)
    sub(el, "type", record.type)
    sub(el, "value", record.value)


def build_bind(cfg: BindConfig) -> etree._Element | None:
    if (
        not cfg.general.enabled
        and not cfg.acls
        and not cfg.domains
        and not cfg.records
        and not cfg.dnsbl.enabled
    ):
        return None

    el = etree.Element("bind")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.general.enabled))
    sub(gen, "disablev6", bool_val(cfg.general.disablev6))
    sub(gen, "enablerpz", bool_val(cfg.general.enablerpz))
    sub(gen, "listenv4", ",".join(cfg.general.listenv4))
    sub(gen, "listenv6", ",".join(cfg.general.listenv6))
    sub(gen, "port", str(cfg.general.port))
    if cfg.general.forwarders:
        sub(gen, "forwarders", ",".join(cfg.general.forwarders))
    sub(gen, "filteraaaav4", bool_val(cfg.general.filteraaaav4))
    sub(gen, "filteraaaav6", bool_val(cfg.general.filteraaaav6))
    if cfg.general.filteraaaaacl:
        sub(gen, "filteraaaaacl", ",".join(cfg.general.filteraaaaacl))
    sub(gen, "logsize", str(cfg.general.logsize))
    sub(gen, "general_log_level", cfg.general.general_log_level)
    sub(gen, "maxcachesize", str(cfg.general.maxcachesize))
    if cfg.general.recursion:
        sub(gen, "recursion", _resolve_acl_uuids(cfg.general.recursion))
    if cfg.general.allowtransfer:
        sub(gen, "allowtransfer", _resolve_acl_uuids(cfg.general.allowtransfer))
    if cfg.general.allowquery:
        sub(gen, "allowquery", _resolve_acl_uuids(cfg.general.allowquery))
    sub(gen, "dnssecvalidation", cfg.general.dnssecvalidation)
    sub(gen, "hidehostname", bool_val(cfg.general.hidehostname))
    sub(gen, "hideversion", bool_val(cfg.general.hideversion))
    sub(gen, "disableprefetch", bool_val(cfg.general.disableprefetch))
    sub(gen, "enableratelimiting", bool_val(cfg.general.enableratelimiting))
    append_if(gen, "ratelimitcount", cfg.general.ratelimitcount)
    if cfg.general.ratelimitexcept:
        sub(gen, "ratelimitexcept", ",".join(cfg.general.ratelimitexcept))
    sub(gen, "rndcalgo", cfg.general.rndcalgo)
    sub(gen, "rndcsecret", cfg.general.rndcsecret)
    append_if(gen, "querysource", cfg.general.querysource or None)
    append_if(gen, "querysourcev6", cfg.general.querysourcev6 or None)
    append_if(gen, "transfersource", cfg.general.transfersource or None)
    append_if(gen, "transfersourcev6", cfg.general.transfersourcev6 or None)

    acl_el = etree.SubElement(el, "acl")
    acls_el = etree.SubElement(acl_el, "acls")
    for acl in cfg.acls:
        _build_acl(acls_el, acl)

    domain_el = etree.SubElement(el, "domain")
    domains_el = etree.SubElement(domain_el, "domains")
    for domain in cfg.domains:
        _build_domain(domains_el, domain)

    record_el = etree.SubElement(el, "record")
    records_el = etree.SubElement(record_el, "records")
    for record in cfg.records:
        _build_record(records_el, record)

    dnsbl_el = etree.SubElement(el, "dnsbl")
    sub(dnsbl_el, "enabled", bool_val(cfg.dnsbl.enabled))
    if cfg.dnsbl.type:
        sub(dnsbl_el, "type", ",".join(cfg.dnsbl.type))
    if cfg.dnsbl.whitelists:
        sub(dnsbl_el, "whitelists", ",".join(cfg.dnsbl.whitelists))
    sub(dnsbl_el, "forcesafegoogle", bool_val(cfg.dnsbl.forcesafegoogle))
    sub(dnsbl_el, "forcesafeduckduckgo", bool_val(cfg.dnsbl.forcesafeduckduckgo))
    sub(dnsbl_el, "forcesafeyoutube", bool_val(cfg.dnsbl.forcesafeyoutube))
    sub(dnsbl_el, "forcestrictbing", bool_val(cfg.dnsbl.forcestrictbing))

    return el
