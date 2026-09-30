from langgraph.graph import END, START, StateGraph

from .nodes import executor, planner
from .state import PlanState


def build_graph():
    graph = StateGraph(PlanState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", END)
    return graph.compile()