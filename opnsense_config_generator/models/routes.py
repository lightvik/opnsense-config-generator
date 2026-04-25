from pydantic import BaseModel, Field


class StaticRoute(BaseModel):
    network: str
    gateway: str
    descr: str = ""
    disabled: bool = False


class RoutesConfig(BaseModel):
    routes: list[StaticRoute] = Field(default_factory=list)
