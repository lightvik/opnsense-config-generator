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
    fargw: bool = False
    priority: int | None = None
    monitor_noroute: bool = False
    monitor_killstates: bool = False
    monitor_killstates_priority: int | None = None
    force_down: bool = False
    latencylow: int | None = None
    latencyhigh: int | None = None
    losslow: int | None = None
    losshigh: int | None = None
    data_length: int | None = None
    nosync: bool = False


class GatewaysConfig(BaseModel):
    gateways: list[Gateway] = Field(default_factory=list)
    default_gw_switch_default: bool = False
