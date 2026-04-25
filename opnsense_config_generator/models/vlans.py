from pydantic import BaseModel, Field


class Vlan(BaseModel):
    if_name: str = Field(alias="if")
    tag: int = Field(ge=1, le=4094)
    pcp: int = Field(default=0, ge=0, le=7)
    descr: str = ""
    vlanif: str = ""

    model_config = {"populate_by_name": True}


class VlansConfig(BaseModel):
    vlans: list[Vlan] = Field(default_factory=list)
