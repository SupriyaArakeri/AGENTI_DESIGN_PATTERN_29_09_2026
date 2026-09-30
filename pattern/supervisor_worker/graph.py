from langgraph.graph import END, START, StateGraph

from .nodes import leaves_balance, math_agent, supervisor
from .state import SupervisorWorkerState


def route(state: SupervisorWorkerState) -> str:
    return "leave" if state.get("worker") == "leave" else "math"


def build_graph():
    graph = StateGraph(SupervisorWorkerState)
    graph.add_node("supervisor", supervisor)
    graph.add_node("math_agent", math_agent)
    graph.add_node("leaves_balance", leaves_balance)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route,
        {"math": "math_agent", "leave": "leaves_balance"},
    )
    graph.add_edge("math_agent", END)
    graph.add_edge("leaves_balance", END)
    return graph.compile()