from typing import Literal

from pydantic import BaseModel, Field


class WebGui(BaseModel):
    protocol: Literal["http", "https"] = "https"
    port: str = ""
    interfaces: str = ""
    nohttpreferercheck: bool = False
    loginautocomplete: bool = False
    ssl_certref: str = ""


class Ssh(BaseModel):
    enabled: bool = False
    # space-separated group names allowed to SSH
    group: str = "admins"
    permitrootlogin: bool = False
    passwordauth: bool = True


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
    # misc
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

    model_config = {"populate_by_name": True}
