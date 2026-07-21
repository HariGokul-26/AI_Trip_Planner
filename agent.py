from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from llm import get_llm

from tools.hotels import search_hotels
from tools.weather import get_weather
from tools.maps import get_distance
from tools.calculator import calculate
from tools.attractions import get_attractions


# =====================================================
# Register Tools
# =====================================================

TOOLS = [
    search_hotels,
    get_weather,
    get_distance,
    calculate,
    get_attractions,
]


TOOL_MAP = {
    tool.name: tool
    for tool in TOOLS
}


# =====================================================
# LLMs
# =====================================================

# Used ONLY for deciding which tools to call

tool_llm = get_llm().bind_tools(TOOLS)


# Used ONLY for generating final response

response_llm = get_llm()



# =====================================================
# Tool Selection Prompt
# =====================================================

TOOL_SYSTEM_PROMPT = """
You are an intelligent AI Travel Planner.

Your responsibility is ONLY to decide which tools should be used.

Available tools:

1. search_hotels

   - Find hotels in a city.
   - Use for accommodation, hotels, ratings,
     prices, facilities or places to stay.


2. get_weather

   - Get the current weather of a city.
   - Use for weather, climate, rain,
     temperature or humidity.


3. get_distance

   - Calculate road distance and travel duration
     between two places.
   - Use for routes, travel time,
     driving distance or navigation.


4. calculate

   - Perform mathematical calculations.
   - Use for travel budgets,
     expense estimation,
     fuel cost,
     percentages,
     arithmetic,
     bill splitting,
     daily expenses,
     or any calculations.


5. get_attractions

   - Find tourist attractions in a city.
   - Use for sightseeing,
     famous places,
     landmarks,
     itinerary planning,
     vacation planning,
     or things to do.


Rules:

- ONLY decide which tool(s) are needed.
- Call one or multiple tools if necessary.
- Continue calling tools until all required information has been collected.
- Never answer using your own knowledge.
- Never summarize.
- Stop only when no further tool calls are required.
"""



# =====================================================
# Final Response Prompt
# =====================================================

FINAL_SYSTEM_PROMPT = """
You are an intelligent AI Travel Planner.

The required tools have already been executed.

Your job is to generate the final response using ONLY
the tool results provided.

General Rules:

- Never call any tools.
- Never invent information.
- Never assume facts that are not present.
- Use only the supplied tool outputs.
- Be friendly, professional and easy to understand.
- Format responses using headings and bullet points whenever appropriate.


If the user asked for:

• Weather
Present the weather neatly along with travel advice.


• Hotels
Recommend the available hotels clearly.


• Attractions
Present the attractions in a readable list.


• Distance
Mention both travel distance and estimated travel duration.


• Budget
Clearly explain the calculation and final amount.


If the user asks for a travel plan or itinerary:

- Create a day-wise itinerary.
- Distribute attractions logically across the requested number of days.
- Mention suitable hotel recommendations if available.
- Mention the weather if available.
- Include budget information if available.
- Keep the itinerary practical and realistic.
- Do not invent attractions, hotels or prices.
- If required information is unavailable, simply omit that section.


Always produce one complete, well-organized response.
"""



# =====================================================
# Agent
# =====================================================

def ask_agent(query: str) -> str:

    """
    Flow:

    User
        ↓
    Tool LLM
        ↓
    Execute Tool(s)
        ↓
    Tool LLM
        ↓
    Execute More Tool(s)
        ↓
    Response LLM
        ↓
    Final Answer
    """



    # =================================================
    # User Query Display
    # =================================================

    print("\n" + "=" * 60)
    print("USER QUERY")
    print("=" * 60)

    print(query)



    messages = [
        SystemMessage(content=TOOL_SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]



    # =================================================
    # Tool Selection
    # =================================================

    ai_message = tool_llm.invoke(messages)

    if not ai_message.tool_calls:

        print("\nNo tool selected.\n")

        return ai_message.content

    print("\n" + "=" * 60)
    print("TOOL EXECUTION")
    print("=" * 60)

    tool_results = []

    for tool_call in ai_message.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\n✔ Tool : {tool_name}")

        print("\nArguments")
        print("-" * 9)
        print(tool_args)

        tool = TOOL_MAP[tool_name]

        result = tool.invoke(tool_args)

        print("\nResult")
        print("-" * 6)
        print(result)

        tool_results.append(result)


    # =================================================
    # Collect Tool Results
    # =================================================

    tool_context = "\n\n".join(tool_results)

    
    # =================================================
    # Final Response Generation
    # =================================================

    final_messages = [

        SystemMessage(
            content=FINAL_SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:
{query}


Tool Results:

{tool_context}
"""
        )

    ]



    print("\n" + "=" * 60)
    print("FINAL LLM RESPONSE")
    print("=" * 60)



    final_response = response_llm.invoke(
        final_messages
    )



    print(final_response.content)



    return final_response.content