from typing import TypedDict


class PlanState(TypedDict, total=False):
    task: str
    plan: list[str]
    output: str