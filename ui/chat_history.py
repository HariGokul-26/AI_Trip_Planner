"""Helpers for managing the in-session conversation list."""

import re
import uuid

import streamlit as st


def make_chat_title(prompt: str) -> str:
    """Return a short, descriptive title instead of repeating the full prompt."""
    text = prompt.strip()
    lower = text.lower()
    patterns = [
        (r"(?:trip|travel)\s+(?:to|in)\s+([a-z][a-z .'-]+)", "Trip to {}"),
        (r"hotels?\s+(?:in|at|near)\s+([a-z][a-z .'-]+)", "Hotels in {}"),
        (r"weather\s+(?:in|for|at)\s+([a-z][a-z .'-]+)", "Weather in {}"),
        (r"attractions?\s+(?:in|at|near)\s+([a-z][a-z .'-]+)", "Attractions in {}"),
    ]
    for pattern, template in patterns:
        match = re.search(pattern, lower)
        if match:
            place = re.sub(r"\b(today|tomorrow|please)\b.*", "", match.group(1)).strip(" .,?!")
            if place:
                return template.format(place.title())
    if any(word in lower for word in ("hotel", "stay", "accommodation")):
        return "Hotel search"
    if any(word in lower for word in ("weather", "rain", "temperature", "forecast")):
        return "Weather forecast"
    if any(word in lower for word in ("attraction", "tourist", "visit", "sightseeing")):
        return "Places to visit"
    if any(word in lower for word in ("budget", "cost", "split", "expense")):
        return "Travel budget"
    if any(word in lower for word in ("distance", "route", "travel time")):
        return "Route planning"
    return "Travel planning chat"


def ensure_chat_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []


def save_active_chat():
    if not st.session_state.messages:
        return
    first_prompt = next(
        (message["content"] for message in st.session_state.messages if message["role"] == "user"),
        "Travel planning chat",
    )
    conversation = {
        "id": st.session_state.active_chat_id,
        "title": make_chat_title(first_prompt),
        "messages": list(st.session_state.messages),
    }
    history = st.session_state.chat_history
    st.session_state.chat_history = [item for item in history if item["id"] != conversation["id"]]
    st.session_state.chat_history.insert(0, conversation)


def start_new_chat():
    save_active_chat()
    st.session_state.active_chat_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.pop("example_prompt", None)


def open_chat(chat_id: str):
    conversation = next((item for item in st.session_state.chat_history if item["id"] == chat_id), None)
    if conversation:
        st.session_state.active_chat_id = conversation["id"]
        st.session_state.messages = list(conversation["messages"])
        st.session_state.pop("example_prompt", None)
