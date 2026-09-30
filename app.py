import streamlit as st

from pattern.tool_using.graph import build_graph


st.set_page_config(page_title="Tool-Using Agent", page_icon="🧮", layout="centered")


@st.cache_resource
def get_workflow():
    return build_graph()


def answer_question(question: str) -> dict[str, str]:
    return get_workflow().invoke({"question": question})


def main() -> None:
    st.title("Tool-Using AI Agent")
    st.caption("Ask an arithmetic question or ask for a clear general explanation.")

    with st.sidebar:
        st.subheader("About this assistant")
        st.write(
            "Arithmetic questions are solved by the reasoning and math agents. "
            "Other questions are answered by the general-response fallback."
        )
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = answer_question(question)
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
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()