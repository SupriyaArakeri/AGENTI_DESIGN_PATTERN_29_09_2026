import streamlit as st

from pattern.tool_using.graph import build_graph
from pattern.planner_executor.graph import build_graph as build_planner_executor_graph
from pattern.supervisor_worker.graph import build_graph as build_supervisor_worker_graph


st.set_page_config(page_title="Agentic AI Patterns", page_icon="🤖", layout="centered")


@st.cache_resource
def get_workflow():
    return build_graph()


@st.cache_resource
def get_planner_executor_workflow():
    return build_planner_executor_graph()


@st.cache_resource
def get_supervisor_worker_workflow():
    return build_supervisor_worker_graph()


def answer_question(question: str) -> dict[str, str]:
    return get_workflow().invoke({"question": question})


def answer_planning_task(task: str) -> dict[str, object]:
    return get_planner_executor_workflow().invoke({"task": task})


def answer_supervisor_query(query: str) -> dict[str, str]:
    return get_supervisor_worker_workflow().invoke({"query": query})


def main() -> None:
    with st.sidebar:
        workflow = st.selectbox(
            "Demonstration",
            ("Tool-Using Agent", "Planner-Executor", "Supervisor-Worker"),
        )
        is_planner_executor = workflow == "Planner-Executor"
        is_supervisor_worker = workflow == "Supervisor-Worker"
        message_key = {
            "Tool-Using Agent": "messages",
            "Planner-Executor": "planner_executor_messages",
            "Supervisor-Worker": "supervisor_worker_messages",
        }[workflow]

        st.subheader("About this pattern")
        if is_planner_executor:
            st.write(
                "The planner breaks a task into up to three steps. The executor "
                "works through each step and returns the combined result."
            )
        elif is_supervisor_worker:
            st.write(
                "A supervisor routes arithmetic requests to the math worker and "
                "leave-balance requests to the leave worker."
            )
        else:
            st.write(
                "Arithmetic questions are solved by the reasoning and math agents. "
                "Other questions are answered by the general-response fallback."
            )
        if st.button("Clear conversation", use_container_width=True):
            st.session_state[message_key] = []
            st.rerun()

    if message_key not in st.session_state:
        st.session_state[message_key] = []

    if is_planner_executor:
        st.title("Planner-Executor")
        st.caption("Turn a task into a short plan, then work through each step.")
        input_label = "Describe a task to plan and execute"
    elif is_supervisor_worker:
        st.title("Supervisor-Worker")
        st.caption("A supervisor picks the specialist best suited to your request.")
        input_label = "Ask a math or leave-balance question"
    else:
        st.title("Tool-Using AI Agent")
        st.caption("Ask an arithmetic question or ask for a clear general explanation.")
        input_label = "Ask a question"

    for message in st.session_state[message_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(input_label)
    if not prompt:
        return

    st.session_state[message_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if is_planner_executor:
                    result = answer_planning_task(prompt)
                    plan = result.get("plan", [])
                    plan_text = "\n".join(plan) if plan else "No plan was generated."
                    output = result.get("output", "No execution output was generated.")
                    answer = f"**Plan**\n\n{plan_text}\n\n**Execution**\n\n{output}"
                elif is_supervisor_worker:
                    result = answer_supervisor_query(prompt)
                    worker = result.get("worker", "unknown")
                    if worker == "leave":
                        answer = (
                            f"**Selected worker:** Leave balance\n\n"
                            f"**Employee:** {result.get('employee_name', 'Unknown')}\n\n"
                            f"**Balance:** {result.get('leave_balance', result.get('result', 'Unavailable'))}"
                        )
                    else:
                        expression = result.get("expression", "")
                        answer = f"**Selected worker:** Math\n\n**Result:** {result.get('result', 'Unavailable')}"
                        if expression:
                            answer += f"\n\nExpression: `{expression}`"
                else:
                    result = answer_question(prompt)
                    if result.get("response"):
                        answer = result["response"]
                    elif result.get("result") is not None:
                        expression = result.get("expression", "")
                        answer = f"**Result:** {result['result']}"
                        if expression:
                            answer += f"\n\nExpression: `{expression}`"
                    else:
                        answer = "I couldn't produce an answer for that request. Please try rephrasing it."
            except Exception as error:
                st.error(
                    "The assistant could not complete the request. Check your API key and "
                    "network connection, then try again."
                )
                answer = f"Request failed: {error}"

        st.markdown(answer)
    st.session_state[message_key].append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()