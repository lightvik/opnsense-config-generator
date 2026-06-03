from typing import Literal

from pydantic import BaseModel, Field


class NatAddress(BaseModel):
    network: str = ""
    address: str = ""
    port: str = ""
    any: bool = False
    invert: bool = False


class OutboundNatRule(BaseModel):
    interface: str = "wan"
    source: NatAddress = Field(default_factory=NatAddress)
    destination: NatAddress = Field(default_factory=lambda: NatAddress(any=True))
    target: str = ""
    targetip: str = ""
    targetip_subnet: int = 0
    descr: str = ""
    disabled: bool = False
    nonat: bool = False
    staticnatport: bool = False
    poolopts: str = ""
    protocol: str = ""
    sourceport: str = ""
    dstport: str = ""
    natport: str = ""
    poolopts_sourcehashkey: str = ""
    log: bool = False
    nosync: bool = False
    ipprotocol: Literal["inet", "inet6"] = "inet"
    tag: str = ""
    tagged: str = ""
    category: str = ""


class PortForward(BaseModel):
    interface: str = "wan"
    protocol: str = "tcp"
    source: NatAddress = Field(default_factory=lambda: NatAddress(any=True))
    destination: NatAddress = Field(default_factory=NatAddress)
    target: str = ""
    local_port: str = Field(default="", alias="local-port")
    descr: str = ""
    disabled: bool = False
    nordr: bool = False
    associated_rule_id: str = Field(
        default="add associated filter rule", alias="associated-rule-id"
    )
    sequence: int | None = None
    ipprotocol: Literal["inet", "inet6", "both"] = "inet"
    poolopts: str = ""
    log: bool = False
    tag: str = ""
    tagged: str = ""
    nosync: bool = False
    natreflection: str = ""
    pass_rule: str = Field(default="", alias="pass")
    category: str = ""

    model_config = {"populate_by_name": True}


class OneToOneNat(BaseModel):
    interface: str = "wan"
    source: NatAddress = Field(default_factory=NatAddress)
    destination: NatAddress = Field(default_factory=NatAddress)
    target: str = ""
    descr: str = ""
    disabled: bool = False


class NatConfig(BaseModel):
    outbound_mode: Literal["automatic", "hybrid", "advanced", "disabled"] = Field(
        default="automatic", alias="outbound_mode"
    )
    outbound_rules: list[OutboundNatRule] = Field(default_factory=list)
    port_forwards: list[PortForward] = Field(default_factory=list)
    one_to_one: list[OneToOneNat] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
