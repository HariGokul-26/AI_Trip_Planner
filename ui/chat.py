import streamlit as st

from agent import ask_agent
from ui.chat_history import save_active_chat


def get_search_status(query: str) -> str:
    """Describe the current work based on the user's request."""
    text = query.lower()
    if any(word in text for word in ("hotel", "stay", "accommodation")):
        return "Finding hotels for your trip..."
    if any(word in text for word in ("attraction", "tourist", "visit", "sightseeing")):
        return "Finding top tourist attractions..."
    if any(word in text for word in ("weather", "rain", "temperature", "forecast")):
        return "Checking the weather forecast..."
    if any(word in text for word in ("distance", "route", "travel time")):
        return "Calculating your route and travel time..."
    if any(word in text for word in ("budget", "cost", "split", "expense")):
        return "Working out your travel budget..."
    if any(word in text for word in ("trip", "itinerary", "plan")):
        return "Building your trip plan..."
    return "Looking into your travel request..."


def render_chat():
    """Render the chat interface."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = None
    if "example_prompt" in st.session_state:
        user_input = st.session_state.example_prompt
        del st.session_state.example_prompt

    typed_input = st.chat_input("Ask anything about your next trip...")
    if typed_input:
        user_input = typed_input

    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner(get_search_status(user_input)):
            response = ask_agent(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    save_active_chat()
    st.rerun()
