from langchain.messages import ToolMessage
from tool import tools_by_name

def tool_node(state: dict):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        obervation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=obervation, tool_call_id=tool_call["id"]))
    return {"messages": result}
