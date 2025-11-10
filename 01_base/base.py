from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from langchain_community.chat_models.tongyi import ChatTongyi

@tool
def search(query: str):
    """用于查询给定城市的天气"""
    if "上海" in query.lower() or "shanghai" in query.lower():
        return "35度，有雾"
    return "30度，晴天" 

tools = [search]

tool_node = ToolNode(tools)
model = ChatTongyi( # type: ignore
    model="qwen-plus",
    model_kwargs={
        "temperature": 0.0,
    }
).bind_tools(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    message = state["messages"]
    last_message = message[-1]
    if last_message.tool_calls:
        return "tools"
    return END
    
def call_model(state: MessagesState):
    message = state["messages"]
    response = model.invoke(message)
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
)

workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()  # could be redis, mongodb, etc

app = workflow.compile(checkpointer=checkpointer)

final_state = app.invoke(
    input={"messages": [HumanMessage(content="上海天气如何？")]},
    config={"configurable": {"thread_id": 42}},
)

result = final_state["messages"][-1].content
print(result)

final_state = app.invoke(
    input={"messages": [HumanMessage(content="我问的哪个城市")]},
    config={"configurable": {"thread_id": 42}},
)
result = final_state["messages"][-1].content
print(result)
