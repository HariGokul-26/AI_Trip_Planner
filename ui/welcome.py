import streamlit as st


def render_welcome():
    """Render the welcome screen before a conversation begins."""
    st.markdown(
        """
        <div class="welcome-card">
        <h1 style="text-align:center;">🌍AI Travel Planner</h1>
        <h4 style="text-align:center; color:gray;">Plan smarter. Travel better.</h4>
        <br>
        <p style="text-align:center;">
            Ask me anything about your next trip. I can help you with hotels, weather,
            attractions, travel distance, and budget planning.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("What I can help with")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Current Weather")
        st.info("Hotel Recommendations")
        st.info("Tourist Attractions")
    with col2:
        st.info("Distance & Travel Time")
        st.info("Budget Calculations")
        st.info("Multi-day Trip Planning")

    st.subheader("Try one of these")
    examples = [
        "Plan a 3 day trip to Kochi",
        "What's the weather in Chennai today?",
        "Find hotels in Ooty",
        "Tourist attractions in Mysore",
        "Distance from Chennai to Pondicherry",
        "Split Rs.18000 across 4 days",
    ]
    cols = st.columns(2)
    for index, prompt in enumerate(examples):
        with cols[index % 2]:
            if st.button(prompt, key=f"example_{index}", use_container_width=True):
                st.session_state.example_prompt = prompt
                st.rerun()
