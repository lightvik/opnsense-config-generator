import pytest
from pydantic import ValidationError

from opnsense_config_generator.models.acme_client import (
    AcmeCertificate,
    AcmeClientConfig,
    AcmeValidation,
)
from opnsense_config_generator.models.aliases import Alias
from opnsense_config_generator.models.bind import BindAcl, BindConfig, BindRecord
from opnsense_config_generator.models.chrony import ChronyConfig
from opnsense_config_generator.models.cron import CronConfig, CronJob
from opnsense_config_generator.models.dnsmasq import DnsmasqConfig, DnsmasqDhcpRange
from opnsense_config_generator.models.filter import FilterRule
from opnsense_config_generator.models.gateways import Gateway
from opnsense_config_generator.models.git_backup import GitBackupConfig
from opnsense_config_generator.models.interfaces import InterfaceConfig
from opnsense_config_generator.models.kea import KeaConfig, KeaDhcpv4Config, KeaSubnet4
from opnsense_config_generator.models.monit import (
    MonitConfig,
    MonitGeneral,
    MonitService,
    MonitTest,
)
from opnsense_config_generator.models.qemu_guest_agent import QemuGuestAgentConfig
from opnsense_config_generator.models.radvd import RadvdConfig, RadvdEntry
from opnsense_config_generator.models.root import OpnSenseConfig
from opnsense_config_generator.models.system import Group, SystemConfig, User
from opnsense_config_generator.models.trafficshaper import (
    ShaperPipe,
    ShaperQueue,
    ShaperRule,
    TrafficShaperConfig,
)
from opnsense_config_generator.models.vlans import Vlan


def test_root_defaults() -> None:
    cfg = OpnSenseConfig()
    assert cfg.system.hostname == "OPNsense"
    assert cfg.system.domain == "internal"


def test_system_from_dict() -> None:
    cfg = SystemConfig(hostname="fw01", domain="home.local")
    assert cfg.hostname == "fw01"


def test_user_requires_name_and_uid() -> None:
    with pytest.raises(ValidationError):
        User(password="x")  # type: ignore[call-arg]


def test_group_requires_name_and_gid() -> None:
    with pytest.raises(ValidationError):
        Group(name="admins")  # type: ignore[call-arg]


def test_vlan_tag_range() -> None:
    with pytest.raises(ValidationError):
        Vlan(**{"if": "vtnet0", "tag": 0})  # tag < 1
    with pytest.raises(ValidationError):
        Vlan(**{"if": "vtnet0", "tag": 4095})  # tag > 4094


def test_interface_config() -> None:
    iface = InterfaceConfig(**{"if": "vtnet0", "ipaddr": "dhcp"})
    assert iface.if_name == "vtnet0"


def test_gateway_weight_range() -> None:
    with pytest.raises(ValidationError):
        Gateway(name="GW", interface="wan", gateway="1.2.3.4", weight=0)
    gw = Gateway(name="GW", interface="wan", gateway="1.2.3.4", weight=1)
    assert gw.weight == 1


def test_alias_type_validated() -> None:
    with pytest.raises(ValidationError):
        Alias(name="test", type="invalid_type")  # type: ignore[arg-type]


def test_filter_rule_defaults() -> None:
    rule = FilterRule()
    assert rule.type == "pass"
    assert rule.interface == "lan"


def test_dnsmasq_range() -> None:
    r = DnsmasqDhcpRange(interface="lan", start_addr="192.168.1.100", end_addr="192.168.1.199")
    assert r.start_addr == "192.168.1.100"
    assert r.end_addr == "192.168.1.199"


def test_dnsmasq_defaults() -> None:
    cfg = DnsmasqConfig()
    assert cfg.enable is False
    assert cfg.port == "53053"


def test_kea_defaults() -> None:
    cfg = KeaConfig()
    assert cfg.dhcp4.enabled is False
    assert cfg.dhcp6.enabled is False
    assert cfg.ctrl_agent.enabled is False
    assert cfg.ddns.enabled is False
    assert cfg.dhcp4.valid_lifetime == 4000
    assert cfg.ctrl_agent.http_port == "8000"
    assert cfg.ddns.server_port == "53001"


def test_kea_dhcp4_subnet() -> None:
    subnet = KeaSubnet4(subnet="10.0.0.0/24")
    assert subnet.option_data_autocollect is True
    assert subnet.pools == []


def test_kea_dhcp4_config() -> None:
    cfg = KeaDhcpv4Config(enabled=True, interfaces=["lan"], subnets=[
        KeaSubnet4(subnet="192.168.1.0/24", pools=["192.168.1.100-192.168.1.200"]),
    ])
    assert cfg.enabled is True
    assert len(cfg.subnets) == 1
    assert cfg.subnets[0].subnet == "192.168.1.0/24"


def test_qemu_guest_agent_defaults() -> None:
    cfg = QemuGuestAgentConfig()
    assert cfg.enabled is False
    assert cfg.log_debug is False
    assert cfg.disabled_rpcs == []


def test_qemu_guest_agent_invalid_rpc() -> None:
    with pytest.raises(ValidationError):
        QemuGuestAgentConfig(enabled=True, disabled_rpcs=["invalid-rpc"])  # type: ignore[list-item]


def test_cron_defaults() -> None:
    cfg = CronConfig()
    assert cfg.jobs == []


def test_cron_job_defaults() -> None:
    job = CronJob(command="firmware update", description="daily update")
    assert job.origin == "cron"
    assert job.enabled is True
    assert job.minutes == "0"
    assert job.hours == "0"
    assert job.days == "*"
    assert job.months == "*"
    assert job.weekdays == "*"
    assert job.who == "root"
    assert job.parameters == ""


def test_cron_job_requires_command_and_description() -> None:
    with pytest.raises(ValidationError):
        CronJob(command="firmware update")  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        CronJob(description="daily update")  # type: ignore[call-arg]


def test_monit_defaults() -> None:
    cfg = MonitConfig()
    assert cfg.general.enabled is False
    assert cfg.general.interval == 120
    assert cfg.general.startdelay == 120
    assert cfg.general.mailserver == "127.0.0.1"
    assert cfg.general.port == 25
    assert cfg.general.ssl is False
    assert cfg.general.sslversion == "auto"
    assert cfg.general.sslverify is True
    assert cfg.general.httpd_enabled is False
    assert cfg.general.httpd_port == 2812
    assert cfg.general.mmonit_timeout == 5
    assert cfg.general.mmonit_register_credentials is True
    assert cfg.alerts == []
    assert cfg.services == []
    assert cfg.tests == []


def test_monit_service_requires_name_and_type() -> None:
    with pytest.raises(ValidationError):
        MonitService(name="nginx")  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        MonitService(type="process")  # type: ignore[call-arg]


def test_monit_service_invalid_type() -> None:
    with pytest.raises(ValidationError):
        MonitService(name="nginx", type="invalid")  # type: ignore[arg-type]


def test_monit_test_invalid_action() -> None:
    with pytest.raises(ValidationError):
        MonitTest(name="t", condition="cpu > 90%", action="invalid")  # type: ignore[arg-type]


def test_monit_general_invalid_sslversion() -> None:
    with pytest.raises(ValidationError):
        MonitGeneral(sslversion="ssl3")  # type: ignore[arg-type]


def test_trafficshaper_defaults() -> None:
    cfg = TrafficShaperConfig()
    assert cfg.pipes == []
    assert cfg.queues == []
    assert cfg.rules == []


def test_trafficshaper_pipe_defaults() -> None:
    pipe = ShaperPipe(number=1, description="WAN", bandwidth=100)
    assert pipe.enabled is True
    assert pipe.bandwidth_metric == "Kbit"
    assert pipe.mask == "none"
    assert pipe.scheduler == ""
    assert pipe.codel_enable is False
    assert pipe.pie_enable is False


def test_trafficshaper_pipe_invalid_metric() -> None:
    with pytest.raises(ValidationError):
        ShaperPipe(number=1, description="WAN", bandwidth=100, bandwidth_metric="GBit")  # type: ignore[arg-type]


def test_trafficshaper_queue_defaults() -> None:
    queue = ShaperQueue(number=1, description="Q1", pipe="WAN")
    assert queue.enabled is True
    assert queue.weight == 100
    assert queue.mask == "none"
    assert queue.codel_enable is False


def test_trafficshaper_rule_defaults() -> None:
    rule = ShaperRule()
    assert rule.enabled is True
    assert rule.sequence == 1
    assert rule.interface == "wan"
    assert rule.proto == "ip"
    assert rule.source == "any"
    assert rule.destination == "any"
    assert rule.direction == ""


def test_trafficshaper_rule_invalid_proto() -> None:
    with pytest.raises(ValidationError):
        ShaperRule(proto="xyz")  # type: ignore[arg-type]


def test_radvd_defaults() -> None:
    cfg = RadvdConfig()
    assert cfg.entries == []


def test_radvd_entry_defaults() -> None:
    entry = RadvdEntry(interface="lan")
    assert entry.enabled is True
    assert entry.mode == "stateless"
    assert entry.dns is True
    assert entry.min_rtr_adv_interval == 200
    assert entry.max_rtr_adv_interval == 600
    assert entry.adv_default_preference == "medium"
    assert entry.adv_cur_hop_limit == 64
    assert entry.rdnss == []
    assert entry.dnssl == []
    assert entry.routes == []


def test_radvd_entry_requires_interface() -> None:
    with pytest.raises(ValidationError):
        RadvdEntry()  # type: ignore[call-arg]


def test_radvd_entry_invalid_mode() -> None:
    with pytest.raises(ValidationError):
        RadvdEntry(interface="lan", mode="invalid")  # type: ignore[arg-type]


def test_radvd_entry_invalid_preference() -> None:
    with pytest.raises(ValidationError):
        RadvdEntry(interface="lan", adv_default_preference="ultra")  # type: ignore[arg-type]


def test_full_minimal_parse() -> None:
    from pathlib import Path

    import yaml
    data = yaml.safe_load((Path(__file__).parent.parent / "golden/minimal/config.yaml").read_text())
    cfg = OpnSenseConfig.model_validate(data)
    assert cfg.system.hostname == "fw01"
    assert "wan" in cfg.interfaces.interfaces
    assert "lan" in cfg.interfaces.interfaces


def test_acme_client_defaults() -> None:
    cfg = AcmeClientConfig()
    assert cfg.settings.enabled is False
    assert cfg.settings.auto_renewal is True
    assert cfg.settings.environment == "prod"
    assert cfg.accounts == []
    assert cfg.certificates == []
    assert cfg.validations == []
    assert cfg.actions == []


def test_acme_certificate_requires_account_and_validation() -> None:
    with pytest.raises(ValidationError):
        AcmeCertificate(name="test.com")  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        AcmeCertificate(name="test.com", account="acct")  # type: ignore[call-arg]


def test_acme_validation_defaults() -> None:
    v = AcmeValidation(name="my-val")
    assert v.method == "dns01"
    assert v.dns_service == "dns_freedns"
    assert v.dns_credentials == {}


def test_acme_validation_invalid_method() -> None:
    with pytest.raises(ValidationError):
        AcmeValidation(name="v", method="ftp01")  # type: ignore[arg-type]


def test_bind_defaults() -> None:
    cfg = BindConfig()
    assert cfg.general.enabled is False
    assert cfg.general.port == 53530
    assert cfg.acls == []
    assert cfg.domains == []
    assert cfg.records == []


def test_bind_acl_requires_networks() -> None:
    with pytest.raises(ValidationError):
        BindAcl(name="test")  # type: ignore[call-arg]


def test_bind_record_requires_domain_and_value() -> None:
    with pytest.raises(ValidationError):
        BindRecord(name="host", type="A")  # type: ignore[call-arg]


def test_chrony_defaults() -> None:
    cfg = ChronyConfig()
    assert cfg.general.enabled is False
    assert cfg.general.port == 323
    assert cfg.general.peers == ["0.opnsense.pool.ntp.org"]
    assert cfg.general.allowed_networks == []


def test_git_backup_defaults() -> None:
    cfg = GitBackupConfig()
    assert cfg.enabled is False
    assert cfg.branch == "master"
    assert cfg.force_push is False
