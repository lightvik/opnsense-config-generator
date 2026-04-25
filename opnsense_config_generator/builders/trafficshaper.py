from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.trafficshaper import TrafficShaperConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _pipe_uuid(description: str) -> str:
    return make_uuid("trafficshaper:pipe", description)


def _queue_uuid(description: str) -> str:
    return make_uuid("trafficshaper:queue", description)


def _rule_uuid(sequence: int, interface: str) -> str:
    return make_uuid("trafficshaper:rule", f"{sequence}:{interface}")


def build_trafficshaper(cfg: TrafficShaperConfig) -> etree._Element | None:
    if not cfg.pipes and not cfg.queues and not cfg.rules:
        return None

    el = etree.Element("TrafficShaper")

    pipes_el = etree.SubElement(el, "pipes")
    for pipe in cfg.pipes:
        uid = _pipe_uuid(pipe.description)
        p = etree.SubElement(pipes_el, "pipe", uuid=uid)
        sub(p, "number", str(pipe.number))
        sub(p, "enabled", bool_val(pipe.enabled))
        sub(p, "bandwidth", str(pipe.bandwidth))
        sub(p, "bandwidthMetric", pipe.bandwidth_metric)
        if pipe.queue is not None:
            sub(p, "queue", str(pipe.queue))
        sub(p, "mask", pipe.mask)
        if pipe.buckets is not None:
            sub(p, "buckets", str(pipe.buckets))
        if pipe.scheduler:
            sub(p, "scheduler", pipe.scheduler)
        sub(p, "codel_enable", bool_val(pipe.codel_enable))
        if pipe.codel_target is not None:
            sub(p, "codel_target", str(pipe.codel_target))
        if pipe.codel_interval is not None:
            sub(p, "codel_interval", str(pipe.codel_interval))
        sub(p, "codel_ecn_enable", bool_val(pipe.codel_ecn_enable))
        sub(p, "pie_enable", bool_val(pipe.pie_enable))
        if pipe.fqcodel_quantum is not None:
            sub(p, "fqcodel_quantum", str(pipe.fqcodel_quantum))
        if pipe.fqcodel_limit is not None:
            sub(p, "fqcodel_limit", str(pipe.fqcodel_limit))
        if pipe.fqcodel_flows is not None:
            sub(p, "fqcodel_flows", str(pipe.fqcodel_flows))
        if pipe.origin:
            sub(p, "origin", pipe.origin)
        if pipe.delay is not None:
            sub(p, "delay", str(pipe.delay))
        sub(p, "description", pipe.description)

    queues_el = etree.SubElement(el, "queues")
    for queue in cfg.queues:
        uid = _queue_uuid(queue.description)
        q = etree.SubElement(queues_el, "queue", uuid=uid)
        sub(q, "number", str(queue.number))
        sub(q, "enabled", bool_val(queue.enabled))
        sub(q, "pipe", _pipe_uuid(queue.pipe))
        sub(q, "weight", str(queue.weight))
        sub(q, "mask", queue.mask)
        if queue.buckets is not None:
            sub(q, "buckets", str(queue.buckets))
        sub(q, "codel_enable", bool_val(queue.codel_enable))
        if queue.codel_target is not None:
            sub(q, "codel_target", str(queue.codel_target))
        if queue.codel_interval is not None:
            sub(q, "codel_interval", str(queue.codel_interval))
        sub(q, "codel_ecn_enable", bool_val(queue.codel_ecn_enable))
        sub(q, "pie_enable", bool_val(queue.pie_enable))
        if queue.origin:
            sub(q, "origin", queue.origin)
        sub(q, "description", queue.description)

    rules_el = etree.SubElement(el, "rules")
    for rule in cfg.rules:
        uid = _rule_uuid(rule.sequence, rule.interface)
        r = etree.SubElement(rules_el, "rule", uuid=uid)
        sub(r, "enabled", bool_val(rule.enabled))
        sub(r, "sequence", str(rule.sequence))
        sub(r, "interface", rule.interface)
        if rule.interface2:
            sub(r, "interface2", rule.interface2)
        sub(r, "proto", rule.proto)
        if rule.iplen is not None:
            sub(r, "iplen", str(rule.iplen))
        sub(r, "source", rule.source)
        sub(r, "source_not", bool_val(rule.source_not))
        sub(r, "src_port", rule.src_port)
        sub(r, "destination", rule.destination)
        sub(r, "destination_not", bool_val(rule.destination_not))
        sub(r, "dst_port", rule.dst_port)
        if rule.dscp:
            sub(r, "dscp", ",".join(rule.dscp))
        if rule.direction:
            sub(r, "direction", rule.direction)
        if rule.target_pipe:
            sub(r, "target", _pipe_uuid(rule.target_pipe))
        elif rule.target_queue:
            sub(r, "target", _queue_uuid(rule.target_queue))
        if rule.description:
            sub(r, "description", rule.description)
        if rule.origin:
            sub(r, "origin", rule.origin)

    return el
