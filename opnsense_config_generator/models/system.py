from typing import Literal

from pydantic import BaseModel, Field


class WebGui(BaseModel):
    protocol: Literal["http", "https"] = "https"
    port: str = ""
    interfaces: str = ""
    nohttpreferercheck: bool = False
    nodnsrebindcheck: bool = False
    loginautocomplete: bool = False
    ssl_certref: str = ""
    authmode: str = ""
    session_timeout: int | None = None
    compression: bool = False
    ssl_ciphers: str = Field(default="", alias="ssl-ciphers")
    ssl_hsts: bool = Field(default=False, alias="ssl-hsts")
    disablehttpredirect: bool = False
    httpaccesslog: bool = False
    noroot: bool = False
    althostnames: str = ""
    quietlogin: bool = False

    model_config = {"populate_by_name": True}


class Ssh(BaseModel):
    enabled: bool = False
    group: str = "admins"
    permitrootlogin: bool = False
    passwordauth: bool = True
    port: str = ""
    interfaces: str = ""
    kex: list[str] = Field(default_factory=list)
    ciphers: list[str] = Field(default_factory=list)
    macs: list[str] = Field(default_factory=list)
    keys: str = ""
    keysig: list[str] = Field(default_factory=list)
    rekeylimit: str = ""


class User(BaseModel):
    name: str
    password: str
    descr: str = ""
    scope: Literal["system", "user"] = "user"
    groupname: str = ""
    uid: int = Field(ge=0)
    shell: str = "/bin/sh"
    expires: str = ""
    comment: str = ""


class Group(BaseModel):
    name: str
    description: str = ""
    scope: Literal["system", "group"] = "group"
    gid: int = Field(ge=0)
    members: list[int] = Field(default_factory=list)
    priv: list[str] = Field(default_factory=list)


class SystemConfig(BaseModel):
    hostname: str = "OPNsense"
    domain: str = "internal"
    dns_servers: list[str] = Field(default_factory=list, alias="dnsserver")
    dnsallowoverride: bool = True
    timezone: str = "Etc/UTC"
    timeservers: str = (
        "0.opnsense.pool.ntp.org 1.opnsense.pool.ntp.org "
        "2.opnsense.pool.ntp.org 3.opnsense.pool.ntp.org"
    )
    optimization: Literal["normal", "high-latency", "aggressive", "conservative"] = "normal"
    webgui: WebGui = Field(default_factory=WebGui)
    ssh: Ssh = Field(default_factory=Ssh)
    users: list[User] = Field(default_factory=list)
    groups: list[Group] = Field(default_factory=list)
    disablenatreflection: Literal["yes", "no"] = "yes"
    usevirtualterminal: bool = True
    disableconsolemenu: bool = False
    ipv6allow: bool = True
    powerd_ac_mode: str = "hadp"
    powerd_battery_mode: str = "hadp"
    powerd_normal_mode: str = "hadp"
    pf_share_forward: bool = True
    lb_use_sticky: bool = True
    rrdbackup: int = -1
    netflowbackup: int = -1
    language: str = ""
    prefer_ipv4: bool = False
    dnslocalhost: bool = False
    dnssearchdomain: str = ""
    dns1gw: str = ""
    dns2gw: str = ""
    dns3gw: str = ""
    dns4gw: str = ""
    dns5gw: str = ""
    dns6gw: str = ""
    dns7gw: str = ""
    dns8gw: str = ""
    gw_switch_default: bool = False
    sudo_allow_wheel: bool = False
    sudo_allow_group: str = ""
    user_allow_gen_token: bool = False
    serialspeed: str = ""
    serialusb: bool = False
    primaryconsole: str = ""
    secondaryconsole: str = ""
    autologout: int | None = None
    deployment: str = ""
    theme: str = ""

    model_config = {"populate_by_name": True}
