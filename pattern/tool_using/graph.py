from langgraph.graph import END, START, StateGraph

from .nodes import (
    classify_question,
    general_agent,
    reasoning_agent,
    route_math_result,
    route_question,
    tool_executor,
)
from .state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify_question", classify_question)
    graph.add_node("reasoning_agent", reasoning_agent)
    graph.add_node("math_agent", tool_executor)
    graph.add_node("general_agent", general_agent)

    graph.add_edge(START, "classify_question")
    graph.add_conditional_edges(
        "classify_question",
        route_question,
        {"math": "reasoning_agent", "general": "general_agent"},
    )
    graph.add_edge("reasoning_agent", "math_agent")
    graph.add_conditional_edges(
        "math_agent",
        route_math_result,
        {"complete": END, "fallback": "general_agent"},
    )
    graph.add_edge("general_agent", END)

    return graph.compile()