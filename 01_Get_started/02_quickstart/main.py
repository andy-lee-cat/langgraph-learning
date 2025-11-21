from agent import agent
from langchain.messages import HumanMessage

messages = [HumanMessage(content="multipy 3312 and 41233.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()
