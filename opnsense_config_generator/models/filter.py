from typing import Literal

from pydantic import BaseModel, Field


class RuleAddress(BaseModel):
    network: str = ""
    address: str = ""
    port: str = ""
    any: bool = False
    invert: bool = False


class FilterRule(BaseModel):
    type: Literal["pass", "block", "reject"] = "pass"
    interface: str = "lan"
    ipprotocol: Literal["inet", "inet6", "inet46"] = "inet"
    protocol: str = ""
    source: RuleAddress = Field(default_factory=RuleAddress)
    destination: RuleAddress = Field(default_factory=lambda: RuleAddress(any=True))
    descr: str = ""
    disabled: bool = False
    log: bool = False
    quick: bool = True
    direction: Literal["in", "out", ""] = "in"
    statetype: Literal["keep state", "synproxy state", "none", ""] = ""
    os: str = ""
    # associated NAT rule
    associated_rule_id: str = Field(default="", alias="associated-rule-id")
    floating: bool = False
    # tracker id (uses UUID in OPNsense)
    tracker: str = ""
    tag: str = ""
    tagged: str = ""
    max: str = ""
    max_src_nodes: str = Field(default="", alias="max-src-nodes")
    max_src_conn: str = Field(default="", alias="max-src-conn")
    max_src_states: str = Field(default="", alias="max-src-states")

    model_config = {"populate_by_name": True}


class FilterConfig(BaseModel):
    rules: list[FilterRule] = Field(default_factory=list)
