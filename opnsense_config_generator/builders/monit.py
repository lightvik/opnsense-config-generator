from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.monit import MonitConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _alert_uuid(recipient: str) -> str:
    return make_uuid("monit:alert", recipient)


def _service_uuid(name: str) -> str:
    return make_uuid("monit:service", name)


def _test_uuid(name: str) -> str:
    return make_uuid("monit:test", name)


def build_monit(cfg: MonitConfig) -> etree._Element | None:
    if not cfg.general.enabled and not cfg.alerts and not cfg.services and not cfg.tests:
        return None

    el = etree.Element("monit")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.general.enabled))
    sub(gen, "interval", str(cfg.general.interval))
    sub(gen, "startdelay", str(cfg.general.startdelay))
    sub(gen, "mailserver", cfg.general.mailserver)
    sub(gen, "port", str(cfg.general.port))
    if cfg.general.username:
        sub(gen, "username", cfg.general.username)
    if cfg.general.password:
        sub(gen, "password", cfg.general.password)
    sub(gen, "ssl", bool_val(cfg.general.ssl))
    sub(gen, "sslversion", cfg.general.sslversion)
    sub(gen, "sslverify", bool_val(cfg.general.sslverify))
    if cfg.general.logfile:
        sub(gen, "logfile", cfg.general.logfile)
    if cfg.general.statefile:
        sub(gen, "statefile", cfg.general.statefile)
    if cfg.general.eventqueue_path:
        sub(gen, "eventqueuePath", cfg.general.eventqueue_path)
    if cfg.general.eventqueue_slots is not None:
        sub(gen, "eventqueueSlots", str(cfg.general.eventqueue_slots))
    sub(gen, "httpdEnabled", bool_val(cfg.general.httpd_enabled))
    sub(gen, "httpdUsername", cfg.general.httpd_username)
    if cfg.general.httpd_password:
        sub(gen, "httpdPassword", cfg.general.httpd_password)
    sub(gen, "httpdPort", str(cfg.general.httpd_port))
    if cfg.general.httpd_allow:
        sub(gen, "httpdAllow", ",".join(cfg.general.httpd_allow))
    if cfg.general.mmonit_url:
        sub(gen, "mmonitUrl", cfg.general.mmonit_url)
    sub(gen, "mmonitTimeout", str(cfg.general.mmonit_timeout))
    sub(gen, "mmonitRegisterCredentials", bool_val(cfg.general.mmonit_register_credentials))

    for alert in cfg.alerts:
        uid = _alert_uuid(alert.recipient)
        a = etree.SubElement(el, "alert", uuid=uid)
        sub(a, "enabled", bool_val(alert.enabled))
        sub(a, "recipient", alert.recipient)
        sub(a, "noton", bool_val(alert.noton))
        if alert.events:
            sub(a, "events", ",".join(alert.events))
        if alert.format:
            sub(a, "format", alert.format)
        if alert.reminder is not None:
            sub(a, "reminder", str(alert.reminder))
        if alert.description:
            sub(a, "description", alert.description)

    for test in cfg.tests:
        uid = _test_uuid(test.name)
        t = etree.SubElement(el, "test", uuid=uid)
        sub(t, "name", test.name)
        sub(t, "type", test.type)
        sub(t, "condition", test.condition)
        sub(t, "action", test.action)
        if test.path:
            sub(t, "path", test.path)

    for svc in cfg.services:
        uid = _service_uuid(svc.name)
        s = etree.SubElement(el, "service", uuid=uid)
        sub(s, "enabled", bool_val(svc.enabled))
        sub(s, "name", svc.name)
        if svc.description:
            sub(s, "description", svc.description)
        sub(s, "type", svc.type)
        if svc.pidfile:
            sub(s, "pidfile", svc.pidfile)
        if svc.match:
            sub(s, "match", svc.match)
        if svc.path:
            sub(s, "path", svc.path)
        sub(s, "timeout", str(svc.timeout))
        sub(s, "starttimeout", str(svc.starttimeout))
        if svc.address:
            sub(s, "address", svc.address)
        if svc.interface:
            sub(s, "interface", svc.interface)
        if svc.start:
            sub(s, "start", svc.start)
        if svc.stop:
            sub(s, "stop", svc.stop)
        if svc.tests:
            sub(s, "tests", ",".join(_test_uuid(t) for t in svc.tests))
        if svc.depends:
            sub(s, "depends", ",".join(_service_uuid(d) for d in svc.depends))
        if svc.polltime:
            sub(s, "polltime", svc.polltime)

    return el
