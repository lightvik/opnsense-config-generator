from pydantic import BaseModel


class GitBackupConfig(BaseModel):
    enabled: bool = False
    url: str = ""
    branch: str = "master"
    force_push: bool = False
    privkey: str = ""
    user: str = ""
    password: str = ""
