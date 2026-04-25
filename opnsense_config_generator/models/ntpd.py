from pydantic import BaseModel, Field


class NtpServer(BaseModel):
    address: str
    pool: bool = False
    prefer: bool = False
    noselect: bool = False


class NtpdConfig(BaseModel):
    servers: list[NtpServer] = Field(default_factory=list)
    interface: str = ""
    orphan: int = 12
