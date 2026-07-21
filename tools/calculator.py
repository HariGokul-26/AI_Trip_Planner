from langchain.tools import tool


@tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Examples:
    - 25000 / 5
    - (18000 + 2500) * 0.18
    - 45 * 12
    """

    try:
        # Disable built-in functions for safety
        result = eval(expression, {"__builtins__": {}}, {})

        return (
            f"Calculation\n"
            f"Expression : {expression}\n"
            f"Result     : {result}"
        )

    except Exception as e:
        return f"Unable to calculate.\nReason: {str(e)}"