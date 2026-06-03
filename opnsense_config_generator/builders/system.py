from lxml import etree

from opnsense_config_generator.models.system import Group, SystemConfig, User
from opnsense_config_generator.password import hash_password
from opnsense_config_generator.xml_utils import sub


def build_system(cfg: SystemConfig) -> etree._Element:
    system = etree.Element("system")

    sub(system, "optimization", cfg.optimization)
    sub(system, "hostname", cfg.hostname)
    sub(system, "domain", cfg.domain)

    if cfg.dnsallowoverride:
        sub(system, "dnsallowoverride", "1")
    sub(system, "dnsallowoverride_exclude")

    for ns in cfg.dns_servers:
        sub(system, "dnsserver", ns)

    _build_groups(system, cfg.groups)
    _build_users(system, cfg.users)

    sub(system, "timezone", cfg.timezone)
    sub(system, "timeservers", cfg.timeservers)

    _build_webgui(system, cfg)
    _build_ssh(system, cfg)

    sub(system, "disablenatreflection", cfg.disablenatreflection)
    if cfg.usevirtualterminal:
        sub(system, "usevirtualterminal", "1")
    if cfg.disableconsolemenu:
        sub(system, "disableconsolemenu")
    if cfg.ipv6allow:
        sub(system, "ipv6allow", "1")

    sub(system, "powerd_ac_mode", cfg.powerd_ac_mode)
    sub(system, "powerd_battery_mode", cfg.powerd_battery_mode)
    sub(system, "powerd_normal_mode", cfg.powerd_normal_mode)

    bogons = etree.SubElement(system, "bogons")
    sub(bogons, "interval", "monthly")

    if cfg.pf_share_forward:
        sub(system, "pf_share_forward", "1")
    if cfg.lb_use_sticky:
        sub(system, "lb_use_sticky", "1")

    sub(system, "rrdbackup", str(cfg.rrdbackup))
    sub(system, "netflowbackup", str(cfg.netflowbackup))

    if cfg.language:
        sub(system, "language", cfg.language)
    if cfg.prefer_ipv4:
        sub(system, "prefer_ipv4")
    if cfg.dnslocalhost:
        sub(system, "dnslocalhost")
    if cfg.dnssearchdomain:
        sub(system, "dnssearchdomain", cfg.dnssearchdomain)
    for i, gw_field in enumerate(
        [
            cfg.dns1gw,
            cfg.dns2gw,
            cfg.dns3gw,
            cfg.dns4gw,
            cfg.dns5gw,
            cfg.dns6gw,
            cfg.dns7gw,
            cfg.dns8gw,
        ],
        start=1,
    ):
        if gw_field:
            sub(system, f"dns{i}gw", gw_field)
    if cfg.gw_switch_default:
        sub(system, "gw_switch_default")
    if cfg.sudo_allow_wheel:
        sub(system, "sudo_allow_wheel")
    if cfg.sudo_allow_group:
        sub(system, "sudo_allow_group", cfg.sudo_allow_group)
    if cfg.user_allow_gen_token:
        sub(system, "user_allow_gen_token")
    if cfg.serialspeed:
        sub(system, "serialspeed", cfg.serialspeed)
    if cfg.serialusb:
        sub(system, "serialusb")
    if cfg.primaryconsole:
        sub(system, "primaryconsole", cfg.primaryconsole)
    if cfg.secondaryconsole:
        sub(system, "secondaryconsole", cfg.secondaryconsole)
    if cfg.autologout is not None:
        sub(system, "autologout", str(cfg.autologout))
    if cfg.deployment:
        sub(system, "deployment", cfg.deployment)
    if cfg.theme:
        sub(system, "theme", cfg.theme)

    return system


def _build_webgui(system: etree._Element, cfg: SystemConfig) -> None:
    wg = etree.SubElement(system, "webgui")
    sub(wg, "protocol", cfg.webgui.protocol)
    if cfg.webgui.port:
        sub(wg, "port", cfg.webgui.port)
    if cfg.webgui.interfaces:
        sub(wg, "interfaces", cfg.webgui.interfaces)
    if cfg.webgui.authmode:
        sub(wg, "authmode", cfg.webgui.authmode)
    if cfg.webgui.session_timeout is not None:
        sub(wg, "session_timeout", str(cfg.webgui.session_timeout))
    if cfg.webgui.nohttpreferercheck:
        sub(wg, "nohttpreferercheck")
    if cfg.webgui.nodnsrebindcheck:
        sub(wg, "nodnsrebindcheck")
    if cfg.webgui.loginautocomplete:
        sub(wg, "loginautocomplete")
    if cfg.webgui.compression:
        sub(wg, "compression")
    if cfg.webgui.ssl_certref:
        sub(wg, "ssl-certref", cfg.webgui.ssl_certref)
    if cfg.webgui.ssl_ciphers:
        sub(wg, "ssl-ciphers", cfg.webgui.ssl_ciphers)
    if cfg.webgui.ssl_hsts:
        sub(wg, "ssl-hsts")
    if cfg.webgui.disablehttpredirect:
        sub(wg, "disablehttpredirect")
    if cfg.webgui.httpaccesslog:
        sub(wg, "httpaccesslog")
    if cfg.webgui.noroot:
        sub(wg, "noroot")
    if cfg.webgui.althostnames:
        sub(wg, "althostnames", cfg.webgui.althostnames)
    if cfg.webgui.quietlogin:
        sub(wg, "quietlogin")


def _build_ssh(system: etree._Element, cfg: SystemConfig) -> None:
    ssh = etree.SubElement(system, "ssh")
    sub(ssh, "group", cfg.ssh.group)
    if cfg.ssh.enabled:
        sub(ssh, "enabled", "enabled")
    if cfg.ssh.permitrootlogin:
        sub(ssh, "permitrootlogin")
    if not cfg.ssh.passwordauth:
        sub(ssh, "nopasswd")
    if cfg.ssh.port:
        sub(ssh, "port", cfg.ssh.port)
    if cfg.ssh.interfaces:
        sub(ssh, "interfaces", cfg.ssh.interfaces)
    if cfg.ssh.kex:
        sub(ssh, "kex", ",".join(cfg.ssh.kex))
    if cfg.ssh.ciphers:
        sub(ssh, "ciphers", ",".join(cfg.ssh.ciphers))
    if cfg.ssh.macs:
        sub(ssh, "macs", ",".join(cfg.ssh.macs))
    if cfg.ssh.keysig:
        sub(ssh, "keysig", ",".join(cfg.ssh.keysig))
    if cfg.ssh.keys:
        sub(ssh, "keys", cfg.ssh.keys)
    if cfg.ssh.rekeylimit:
        sub(ssh, "rekeylimit", cfg.ssh.rekeylimit)


def _build_groups(system: etree._Element, groups: list[Group]) -> None:
    for group in groups:
        g = etree.SubElement(system, "group")
        sub(g, "name", group.name)
        sub(g, "description", group.description)
        sub(g, "scope", group.scope)
        sub(g, "gid", str(group.gid))
        for member in group.members:
            sub(g, "member", str(member))
        for priv in group.priv:
            sub(g, "priv", priv)


def _build_users(system: etree._Element, users: list[User]) -> None:
    for user in users:
        u = etree.SubElement(system, "user")
        sub(u, "name", user.name)
        sub(u, "descr", user.descr)
        sub(u, "scope", user.scope)
        if user.groupname:
            sub(u, "groupname", user.groupname)
        # plaintext → bcrypt hash, never store plaintext in XML
        password_hash = (
            user.password if user.password.startswith("$2") else hash_password(user.password)
        )
        sub(u, "password", password_hash)
        sub(u, "uid", str(user.uid))
        if user.shell:
            sub(u, "shell", user.shell)
        if user.expires:
            sub(u, "expires", user.expires)
