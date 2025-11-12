from langchain_community.chat_models.tongyi import ChatTongyi

llm = ChatTongyi( # type: ignore
    model="qwen-max",
    model_kwargs={
        "temperature": 0.0,
        "enable_thinking": False,
    },
)
