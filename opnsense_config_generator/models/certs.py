from pydantic import BaseModel, Field


class CaEntry(BaseModel):
    descr: str
    crt: str = ""  # base64-encoded PEM certificate
    prv: str = ""  # base64-encoded PEM private key
    serial: int = 0
    caref: str = ""  # refid of parent CA (for intermediate CAs)


class CertEntry(BaseModel):
    descr: str
    crt: str = ""  # base64-encoded PEM certificate
    prv: str = ""  # base64-encoded PEM private key
    caref: str = ""  # refid of signing CA; empty = self-signed


class CertsConfig(BaseModel):
    ca: list[CaEntry] = Field(default_factory=list)
    cert: list[CertEntry] = Field(default_factory=list)
