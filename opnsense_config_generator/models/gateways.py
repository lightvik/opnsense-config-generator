from typing import Literal

from pydantic import BaseModel, Field


class Gateway(BaseModel):
    name: str
    interface: str
    gateway: str
    descr: str = ""
    defaultgw: bool = False
    monitor_disable: bool = False
    monitor: str = ""
    weight: int = Field(default=1, ge=1, le=30)
    interval: int = Field(default=1, ge=1)
    loss_interval: int = Field(default=2, ge=1)
    time_period: int = Field(default=60, ge=1)
    alert_interval: int = Field(default=1, ge=1)
    ipprotocol: Literal["inet", "inet6"] = "inet"


class GatewaysConfig(BaseModel):
    gateways: list[Gateway] = Field(default_factory=list)
    default_gw_switch_default: bool = False
