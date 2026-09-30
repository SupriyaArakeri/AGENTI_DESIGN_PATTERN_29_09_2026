import unittest
from unittest.mock import patch

from pattern.supervisor_worker import nodes
from pattern.supervisor_worker.graph import build_graph


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, *responses: str):
        self.responses = iter(responses)

    def invoke(self, _prompt: str) -> FakeMessage:
        return FakeMessage(next(self.responses))


class SupervisorWorkerTests(unittest.TestCase):
    def test_routes_math_query_to_math_worker(self):
        fake_llm = FakeLLM("math", "(10 + 5) / 2")
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke({"query": "What is the average of 10 and 5?"})

        self.assertEqual(result["worker"], "math")
        self.assertEqual(result["expression"], "(10 + 5) / 2")
        self.assertEqual(result["result"], "7.5")

    def test_routes_leave_query_to_leave_worker(self):
        fake_llm = FakeLLM("leave", "Alice")
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke({"query": "What is the leave balance for Alice?"})

        self.assertEqual(result["worker"], "leave")
        self.assertEqual(result["employee_name"], "Alice")
        self.assertEqual(result["leave_balance"], "12 days")


if __name__ == "__main__":
    unittest.main()