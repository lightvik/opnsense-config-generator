from lxml import etree

from opnsense_config_generator.models.gateways import GatewaysConfig
from opnsense_config_generator.xml_utils import sub


def build_gateways(cfg: GatewaysConfig) -> etree._Element | None:
    if not cfg.gateways:
        return None
    gateways = etree.Element("gateways")
    for gw in cfg.gateways:
        g = etree.SubElement(gateways, "gateway_item")
        sub(g, "name", gw.name)
        sub(g, "interface", gw.interface)
        sub(g, "gateway", gw.gateway)
        sub(g, "ipprotocol", gw.ipprotocol)
        if gw.descr:
            sub(g, "descr", gw.descr)
        if gw.defaultgw:
            sub(g, "defaultgw")
        if gw.monitor_disable:
            sub(g, "monitor_disable")
        elif gw.monitor:
            sub(g, "monitor", gw.monitor)
        sub(g, "weight", str(gw.weight))
        sub(g, "interval", str(gw.interval))
        sub(g, "loss_interval", str(gw.loss_interval))
        sub(g, "time_period", str(gw.time_period))
        sub(g, "alert_interval", str(gw.alert_interval))
        if gw.latencylow is not None:
            sub(g, "latencylow", str(gw.latencylow))
        if gw.latencyhigh is not None:
            sub(g, "latencyhigh", str(gw.latencyhigh))
        if gw.losslow is not None:
            sub(g, "losslow", str(gw.losslow))
        if gw.losshigh is not None:
            sub(g, "losshigh", str(gw.losshigh))
        if gw.data_length is not None:
            sub(g, "data_length", str(gw.data_length))
        if gw.priority is not None:
            sub(g, "priority", str(gw.priority))
        if gw.fargw:
            sub(g, "fargw")
        if gw.monitor_noroute:
            sub(g, "monitor_noroute")
        if gw.monitor_killstates:
            sub(g, "monitor_killstates")
        if gw.monitor_killstates_priority is not None:
            sub(g, "monitor_killstates_priority", str(gw.monitor_killstates_priority))
        if gw.force_down:
            sub(g, "force_down")
        if gw.nosync:
            sub(g, "nosync")
    return gateways
