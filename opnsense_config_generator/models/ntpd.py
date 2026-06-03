from pydantic import BaseModel, Field


class NtpServer(BaseModel):
    address: str
    pool: bool = False
    prefer: bool = False
    noselect: bool = False
    iburst: bool = False


class NtpdConfig(BaseModel):
    servers: list[NtpServer] = Field(default_factory=list)
    interface: str = ""
    orphan: int = 12
    clientmode: bool = False
    clockstats: bool = False
    kod: bool = False
    limited: bool = False
    logpeer: bool = False
    logsys: bool = False
    loopstats: bool = False
    peerstats: bool = False
    maxclock: int | None = None
    nomodify: bool = False
    nopeer: bool = False
    noserve: bool = False
    notrap: bool = False
    query: bool = False
    statsgraph: bool = False
    custom_options: str = ""
    leapsec: str = ""
