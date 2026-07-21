import streamlit as st

from ui.chat_history import open_chat, start_new_chat


def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.title("🌍AI Travel Planner")
        st.caption("Your AI-powered travel assistant")
        st.divider()

        if st.button("New Chat", use_container_width=True):
            start_new_chat()
            st.rerun()

        if st.session_state.chat_history:
            st.subheader("Recent chats")
            for conversation in st.session_state.chat_history:
                is_active = conversation["id"] == st.session_state.active_chat_id
                if st.button(
                    conversation["title"],
                    key=f"chat_{conversation['id']}",
                    use_container_width=True,
                    disabled=is_active,
                ):
                    open_chat(conversation["id"])
                    st.rerun()

        st.divider()
        st.subheader("Capabilities")
        st.markdown("""
- Weather Forecast
- Hotel Recommendations
- Tourist Attractions
- Distance & Travel Time
- Budget Calculator
- Multi-day Trip Planning
""")

        st.divider()
        st.subheader("Try Asking")
        for example in [
            "Plan a 5 day trip to Kochi",
            "Find hotels in Ooty",
            "What's the weather in Chennai today?",
            "Tourist attractions in Mysore",
            "Distance from Chennai to Pondicherry",
            "Split Rs.18000 across 4 days",
        ]:
            st.markdown(f"- {example}")

        st.divider()
        st.subheader("About")
        st.markdown("""
This application helps you plan trips using AI.

It can find hotels, check weather, discover attractions, calculate travel budgets,
and estimate travel distance.
""")
