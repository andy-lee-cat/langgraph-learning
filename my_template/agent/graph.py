from typing import Literal
from typing_extensions import TypedDict, Annotated
import operator

from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models.tongyi import ChatTongyi

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """决定是否需要继续调用工具or结束"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

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

model = ChatTongyi(  # type: ignore
    model="qwen-max",
    model_kwargs={
        "temperature": 0.0,
        "enable_thinking": False,
    }
)
model_with_tools = model.bind_tools(tools)

def llm_node(state: dict):
    """LLM 决定是否要调用工具"""
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="你是一个热心的助手来回答数学问题，但你对于加减乘除的计算不是特别擅长，如果需要计算，请调用工具。"
                    )
                ]
                + state["messages"]
            )
        ]
    } 

def tool_node(state: dict):
    """调用工具"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        obervation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=obervation, tool_call_id=tool_call["id"]))
    return {"messages": result}

agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_node", llm_node)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_node")
agent_builder.add_conditional_edges(
    "llm_node",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_node")

agent = agent_builder.compile()

if __name__ == "__main__":
    messages = [HumanMessage(content="multipy 3312 and 41233.")]
    messages = agent.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()
