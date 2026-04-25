from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.cron import CronConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _job_uuid(command: str, description: str) -> str:
    return make_uuid("cron:job", f"{command}:{description}")


def build_cron(cfg: CronConfig) -> etree._Element | None:
    if not cfg.jobs:
        return None

    el = etree.Element("cron")
    jobs_el = etree.SubElement(el, "jobs")

    for job in cfg.jobs:
        uid = _job_uuid(job.command, job.description)
        j = etree.SubElement(jobs_el, "job", uuid=uid)
        sub(j, "origin", job.origin)
        sub(j, "enabled", bool_val(job.enabled))
        sub(j, "minutes", job.minutes)
        sub(j, "hours", job.hours)
        sub(j, "days", job.days)
        sub(j, "months", job.months)
        sub(j, "weekdays", job.weekdays)
        sub(j, "who", job.who)
        sub(j, "command", job.command)
        if job.parameters:
            sub(j, "parameters", job.parameters)
        sub(j, "description", job.description)

    return el
