from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    intent: str
    expression: str
    result: str
    response: str
    error: str