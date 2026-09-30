import unittest
from unittest.mock import patch

from pattern.tool_using.graph import build_graph
from pattern.tool_using import nodes
from tools.calculator import calculator


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, *responses: str):
        self.responses = iter(responses)

    def invoke(self, _prompt: str) -> FakeMessage:
        return FakeMessage(next(self.responses))


class CalculatorTests(unittest.TestCase):
    def test_evaluates_arithmetic(self):
        self.assertEqual(calculator("((10 + 5) / 2) ** 2"), "56.25")

    def test_rejects_non_arithmetic_expressions(self):
        with self.assertRaises(ValueError):
            calculator("__import__('os').system('echo unsafe')")


class WorkflowTests(unittest.TestCase):
    def test_general_question_uses_general_agent(self):
        fake_llm = FakeLLM("GENERAL", "AI is the field of building systems that perform tasks associated with intelligence.")
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke({"question": "Define AI"})

        self.assertIn("field of building systems", result["response"])
        self.assertNotIn("result", result)

    def test_arithmetic_question_uses_math_agent(self):
        fake_llm = FakeLLM("MATH", "((10 + 5) / 2) ** 2")
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke(
                {"question": "What is the square of the average of 10 and 5?"}
            )

        self.assertEqual(result["result"], "56.25")

    def test_invalid_math_expression_falls_back_to_general_agent(self):
        fake_llm = FakeLLM("MATH", "not a Python expression", "Here is the explanation.")
        with patch.object(nodes, "llm", fake_llm):
            result = build_graph().invoke({"question": "Explain this calculation"})

        self.assertEqual(result["response"], "Here is the explanation.")
        self.assertEqual(result["error"], "")


if __name__ == "__main__":
    unittest.main()