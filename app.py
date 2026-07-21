import streamlit as st

from ui.styles import load_css
from ui.sidebar import render_sidebar
from ui.welcome import render_welcome
from ui.chat import render_chat
from ui.chat_history import ensure_chat_state


# Streamlit stores the last sidebar choice in the browser. On each new app
# session, initialize it once in the opposite state before applying the real
# default so a previously collapsed sidebar does not carry over after restart.
if "sidebar_startup_reset" not in st.session_state:
    st.set_page_config(
        page_title="AI Travel Planner",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.session_state.sidebar_startup_reset = True
    st.rerun()

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="globe_with_meridians",
    layout="wide",
    initial_sidebar_state="expanded",
)


load_css()
ensure_chat_state()
render_sidebar()

if len(st.session_state.messages) == 0:
    render_welcome()

render_chat()
