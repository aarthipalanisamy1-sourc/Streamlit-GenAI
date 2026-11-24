
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()


# Streamlit page setup
st.set_page_config(
    page_title="ChatBot",
    page_icon="📖",
    layout="centered",
)


# --------------------------------
# UI Styling
# --------------------------------

st.markdown("""
<style>

/* Background color */
.stApp {
    background-color: #F5F8FC;
}

/* Heading color */
h1 {
    color: #2563EB;
    text-align: center;
    font-size: 32px;
}

/* Chat message border */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #D6E4F0;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

/* Chat input border */
[data-testid="stChatInput"] {
    border: 1px solid #93C5FD;
    border-radius: 12px;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #EFF6FF;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# Initialize Chat History
# --------------------------------

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# --------------------------------
# Sidebar - Recent History
# --------------------------------

with st.sidebar:

    st.title("📚 Recent History")
    st.divider()

    user_messages = [
        message["content"]
        for message in st.session_state["chat_history"]
        if message["role"] == "user"
    ]

    if user_messages:

        for i, question in enumerate(
            reversed(user_messages[-5:]), 1
        ):
            st.markdown(f"**{i}.** {question}")

    else:
        st.caption("No recent conversations yet.")

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()


# --------------------------------
# Main Heading
# --------------------------------

st.title("👥💬 Generative AI ChatBot")
st.caption("✨ Your friendly AI assistant")
st.divider()


# --------------------------------
# Show Chat History
# --------------------------------

for message in st.session_state["chat_history"]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# LLM Initialization
# --------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
)


# --------------------------------
# Chat Input
# --------------------------------

user_prompt = st.chat_input(
    "👋 Hi! What would you like to know?"
)


if user_prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("✨ Thinking..."):

            try:

                response = llm.invoke(
                    input=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant."
                        },
                        *st.session_state.chat_history
                    ]
                )

                assistant_response = response.content

                st.markdown(assistant_response)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except Exception as e:

                st.error(f"Something went wrong: {e}")
