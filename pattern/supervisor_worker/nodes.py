from config.llm import get_llm
from tools.calculator import calculator
from tools.leaves_db import get_leave_balance

from .state import SupervisorWorkerState

llm = None


def _get_llm():
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def supervisor(state: SupervisorWorkerState) -> dict[str, str]:
    prompt = f"""Choose the best worker for the request.
Return exactly one word: math or leave.
Choose math for calculations, percentages, averages, or totals.
Choose leave for leave balance, vacation, sick leave, or PTO questions.

Request: {state['query']}
Worker:"""
    selection = _get_llm().invoke(prompt).content.strip().lower()
    worker = "leave" if "leave" in selection else "math"
    return {"worker": worker}


def math_agent(state: SupervisorWorkerState) -> dict[str, str]:
    prompt = f"""Convert this request into a valid Python arithmetic expression.
Return only the expression, without explanation or code fences.

Request: {state['query']}
Expression:"""
    expression = _get_llm().invoke(prompt).content.strip()
    try:
        result = calculator(expression)
    except (ArithmeticError, ValueError) as error:
        result = f"Error: {error}"
    return {"expression": expression, "result": result}


def leaves_balance(state: SupervisorWorkerState) -> dict[str, str]:
    prompt = f"""Extract only the employee's name from this leave-balance request.

Request: {state['query']}
Employee name:"""
    employee_name = _get_llm().invoke(prompt).content.strip()
    balance = get_leave_balance(employee_name)
    return {
        "employee_name": employee_name,
        "leave_balance": balance,
        "result": balance,
    }