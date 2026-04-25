from typing import Literal

from pydantic import BaseModel, Field

BandwidthMetric = Literal["bit", "Kbit", "Mbit", "Gbit"]
PipeMask = Literal["none", "src-ip", "dst-ip", "src-ip6", "dst-ip6"]
Scheduler = Literal["", "fifo", "rr", "qfq", "fq_codel", "fq_pie"]
Proto = Literal["ip", "ip4", "ip6", "udp", "tcp", "tcp_ack", "tcp_ack_not", "icmp", "ipv6-icmp", "igmp", "esp", "ah", "gre"]
Direction = Literal["", "in", "out"]


class ShaperPipe(BaseModel):
    number: int
    description: str
    enabled: bool = True
    bandwidth: int
    bandwidth_metric: BandwidthMetric = "Kbit"
    queue: int | None = None
    mask: PipeMask = "none"
    buckets: int | None = None
    scheduler: Scheduler = ""
    codel_enable: bool = False
    codel_target: int | None = None
    codel_interval: int | None = None
    codel_ecn_enable: bool = False
    pie_enable: bool = False
    fqcodel_quantum: int | None = None
    fqcodel_limit: int | None = None
    fqcodel_flows: int | None = None
    origin: str = ""
    delay: int | None = None


class ShaperQueue(BaseModel):
    number: int
    description: str
    pipe: str  # description of parent pipe — resolved to UUID in builder
    enabled: bool = True
    weight: int = 100
    mask: PipeMask = "none"
    buckets: int | None = None
    codel_enable: bool = False
    codel_target: int | None = None
    codel_interval: int | None = None
    codel_ecn_enable: bool = False
    pie_enable: bool = False
    origin: str = ""


class ShaperRule(BaseModel):
    enabled: bool = True
    sequence: int = 1
    interface: str = "wan"
    interface2: str = ""
    proto: Proto = "ip"
    iplen: int | None = None
    source: str = "any"
    source_not: bool = False
    src_port: str = "any"
    destination: str = "any"
    destination_not: bool = False
    dst_port: str = "any"
    dscp: list[str] = Field(default_factory=list)
    direction: Direction = ""
    target_pipe: str = ""
    target_queue: str = ""
    description: str = ""
    origin: str = ""


class TrafficShaperConfig(BaseModel):
    pipes: list[ShaperPipe] = Field(default_factory=list)
    queues: list[ShaperQueue] = Field(default_factory=list)
    rules: list[ShaperRule] = Field(default_factory=list)
