from config.llm import get_llm

from .state import PlanState

llm = None


def _get_llm():
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def planner(state: PlanState) -> dict[str, list[str]]:
    prompt = f"""You are a planning agent.
Break the task into at most 3 clear, actionable steps.
Each step must start with a dash (-). Return only the steps, with no introduction.

Task: {state['task']}
Plan:"""
    response = _get_llm().invoke(prompt).content.strip()
    plan = [line.strip() for line in response.splitlines() if line.strip().startswith("-")]
    return {"plan": plan}


def executor(state: PlanState) -> dict[str, str]:
    results = []
    for step in state["plan"]:
        prompt = f"""Complete this step clearly and concisely. Provide a useful result,
not instructions about how another agent could complete it.

Step: {step}
Result:"""
        results.append(_get_llm().invoke(prompt).content.strip())

    return {"output": "\n\n".join(results)}