from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_template(
    """
You are an expert travel planner.

Plan a {days}-day trip to {destination}.

The total budget is ₹{budget}.

Provide:

1. Best places to visit
2. Suggested hotels
3. Local food
4. Travel tips
"""
)