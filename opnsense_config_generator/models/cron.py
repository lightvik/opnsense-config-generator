from pydantic import BaseModel, Field


class CronJob(BaseModel):
    origin: str = "cron"
    enabled: bool = True
    minutes: str = "0"
    hours: str = "0"
    days: str = "*"
    months: str = "*"
    weekdays: str = "*"
    who: str = "root"
    command: str
    parameters: str = ""
    description: str


class CronConfig(BaseModel):
    jobs: list[CronJob] = Field(default_factory=list)
