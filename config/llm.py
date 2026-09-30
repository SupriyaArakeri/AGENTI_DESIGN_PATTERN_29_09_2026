from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm(temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)