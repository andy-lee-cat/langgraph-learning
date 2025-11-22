# Use time-travel

## intro

检查workflow的运行过程，langgraph提供了从检查点checkpoint恢复执行的功能。

详细文档：[time-travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)

使用流程：

1. 使用invoke或stream根据初始输入来运行graph
2. 使用get_state_history来检索特定thread_id的运行历史，找到所需的checkpoint
3. （可选）更新checkpoint对应的state
4. 使用invoke或stream，输入None，配置相应thread_id和checkpoint_id来恢复运行
