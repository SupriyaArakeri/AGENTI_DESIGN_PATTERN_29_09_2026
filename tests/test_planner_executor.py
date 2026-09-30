import unittest
from unittest.mock import patch

from pattern.planner_executor import nodes
from pattern.planner_executor.graph import build_graph


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, *responses: str):
        self.responses = iter(responses)

    def invoke(self, _prompt: str) -> FakeMessage:
        return FakeMessage(next(self.responses))


class PlannerExecutorTests(unittest.TestCase):
    def test_graph_plans_and_executes_task(self):
        fake_llm = FakeLLM(
            "- Research target users\n- Prototype the chatbot\n- Launch a pilot",
            "Define the primary user groups and their needs.",
            "Build a small working prototype and gather feedback.",
            "Release it to a limited group and review their feedback.",
        )
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke({"task": "Launch an AI chatbot"})

        self.assertEqual(
            result["plan"],
            [
                "- Research target users",
                "- Prototype the chatbot",
                "- Launch a pilot",
            ],
        )
        self.assertIn("Define the primary user groups", result["output"])
        self.assertIn("Release it to a limited group", result["output"])


if __name__ == "__main__":
    unittest.main()