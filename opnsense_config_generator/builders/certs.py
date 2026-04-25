from lxml import etree

from opnsense_config_generator.models.certs import CaEntry, CertEntry, CertsConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def refid(kind: str, descr: str) -> str:
    """Deterministic 8-char hex refid, stable across renders."""
    return make_uuid(kind, descr).replace("-", "")[:8]


def build_cas(cas: list[CaEntry]) -> list[etree._Element]:
    elements = []
    for ca in cas:
        el = etree.Element("ca")
        sub(el, "refid", refid("ca", ca.descr))
        sub(el, "descr", ca.descr)
        if ca.caref:
            sub(el, "caref", ca.caref)
        if ca.crt:
            sub(el, "crt", ca.crt)
        if ca.prv:
            sub(el, "prv", ca.prv)
        sub(el, "serial", str(ca.serial))
        elements.append(el)
    return elements


def build_certs(certs: list[CertEntry]) -> list[etree._Element]:
    elements = []
    for cert in certs:
        el = etree.Element("cert")
        sub(el, "refid", refid("cert", cert.descr))
        sub(el, "descr", cert.descr)
        if cert.caref:
            sub(el, "caref", cert.caref)
        if cert.crt:
            sub(el, "crt", cert.crt)
        if cert.prv:
            sub(el, "prv", cert.prv)
        elements.append(el)
    return elements


def build_certs_config(cfg: CertsConfig) -> tuple[list[etree._Element], list[etree._Element]]:
    return build_cas(cfg.ca), build_certs(cfg.cert)
