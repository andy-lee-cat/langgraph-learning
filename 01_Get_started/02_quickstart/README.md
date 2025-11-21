# quickstart

官方教程[text](https://docs.langchain.com/oss/python/langgraph/quickstart)

llm调用替换为第三方库的qwen实现。

一个简单的llm示例，llm会先判断一下是否要调用工具，如果需要，构造调用工具的参数，调用工具，然后再进行llm的回复，否则直接进行回复。

这个流程用agent的一个循环来实现。should_continue里面写的更复杂就可以是一个复杂的agent了，这里should_continue写的是要调用工具为True，否则为False。
