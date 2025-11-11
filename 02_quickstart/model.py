from langchain_community.chat_models.tongyi import ChatTongyi
from tool import tools

# Use a small model that can't reason on its own. Then you can use a tool with fake answers to check the tool calls.
model = ChatTongyi( # type: ignore
    model="qwen3-0.6b",
    model_kwargs={
        "temperature": 0.0,
        "enable_thinking": False,
    },
)

model_with_tools = model.bind_tools(tools)