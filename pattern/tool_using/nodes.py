from config.llm import get_llm
from tools.calculator import calculator

from .state import AgentState

llm = None


def _get_llm():
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def classify_question(state: AgentState) -> dict[str, str]:
    prompt = f"""Classify the user's request for a two-agent assistant.
Return exactly MATH if the request can be answered by evaluating a numeric arithmetic expression.
Return exactly GENERAL for definitions, explanations, advice, or any other request.

User request: {state['question']}
Classification:"""
    classification = _get_llm().invoke(prompt).content.strip().lower()
    intent = "math" if classification.startswith("math") else "general"
    return {"intent": intent}


def reasoning_agent(state: AgentState) -> dict[str, str]:
    prompt = f"""Convert this arithmetic question into one valid Python arithmetic expression.
Return only the expression. Do not include prose, code fences, names, or function calls.

Question: {state['question']}
Expression:"""
    expression = _get_llm().invoke(prompt).content.strip()
    return {"expression": expression}


def tool_executor(state: AgentState) -> dict[str, str]:
    try:
        return {"result": calculator(state["expression"]), "error": ""}
    except (ArithmeticError, ValueError) as error:
        return {"error": str(error)}


def general_agent(state: AgentState) -> dict[str, str]:
    prompt = f"""Answer the user's request clearly and accurately. If it is outside your knowledge,
say so rather than inventing details.

User request: {state['question']}
Answer:"""
    response = _get_llm().invoke(prompt).content.strip()
    return {"response": response, "error": ""}


def route_question(state: AgentState) -> str:
    return "math" if state.get("intent") == "math" else "general"


def route_math_result(state: AgentState) -> str:
    return "fallback" if state.get("error") else "complete"