from langchain.tools import tool

# define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add `a` and `b`.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    """
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        """
    return a / b

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}