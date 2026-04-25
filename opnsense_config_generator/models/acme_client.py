from typing import Literal

from pydantic import BaseModel, Field

AcmeCa = Literal[
    "buypass", "buypass_test", "google", "google_test",
    "letsencrypt", "letsencrypt_test", "sslcom", "zerossl", "custom",
]
AcmeKeyLength = Literal["key_2048", "key_3072", "key_4096", "key_ec256", "key_ec384"]
AcmeAliasMode = Literal["none", "automatic", "domain", "challenge"]
AcmeValidationMethod = Literal["http01", "dns01", "tlsalpn01"]
AcmeLogLevel = Literal["normal", "extended", "debug", "debug2", "debug3"]
AcmeEnvironment = Literal["prod", "stg"]


class AcmeSettings(BaseModel):
    enabled: bool = False
    auto_renewal: bool = True
    environment: AcmeEnvironment = "prod"
    challenge_port: int = 43580
    tls_challenge_port: int = 43581
    restart_timeout: int = 600
    log_level: AcmeLogLevel = "normal"


class AcmeAccount(BaseModel):
    name: str
    enabled: bool = True
    description: str = ""
    email: str = ""
    ca: AcmeCa = "letsencrypt"
    custom_ca: str = ""
    eab_kid: str = ""
    eab_hmac: str = ""


class AcmeCertificate(BaseModel):
    name: str
    enabled: bool = True
    description: str = ""
    alt_names: list[str] = Field(default_factory=list)
    account: str
    validation_method: str
    key_length: AcmeKeyLength = "key_4096"
    ocsp: bool = False
    restart_actions: list[str] = Field(default_factory=list)
    auto_renewal: bool = True
    renew_interval: int = 60
    aliasmode: AcmeAliasMode = "none"
    domain_alias: str = ""
    challenge_alias: str = ""


class AcmeValidation(BaseModel):
    name: str
    enabled: bool = True
    description: str = ""
    method: AcmeValidationMethod = "dns01"
    dns_service: str = "dns_freedns"
    dns_sleep: int = 0
    dns_credentials: dict[str, str] = Field(default_factory=dict)


class AcmeAction(BaseModel):
    name: str
    enabled: bool = True
    description: str = ""
    type: str
    extra_params: dict[str, str] = Field(default_factory=dict)


class AcmeClientConfig(BaseModel):
    settings: AcmeSettings = Field(default_factory=AcmeSettings)
    accounts: list[AcmeAccount] = Field(default_factory=list)
    certificates: list[AcmeCertificate] = Field(default_factory=list)
    validations: list[AcmeValidation] = Field(default_factory=list)
    actions: list[AcmeAction] = Field(default_factory=list)
