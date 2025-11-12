# 03_thinking_in_langgraph

官方教程[text](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)

## 核心要点

工作流程拆分：把逻辑拆分成一个个独立步骤，构造一个图。

每个节点捆绑了一个函数，用return的Command(update={key:value}, goto=goto)的goto来标志前往的下一个节点的str类型字符串名。

函数返回值使用类型主食`Command[Literal["node1", "node2"]]`

函数内不return Command是静态路由，在构造图的时候写好下一个节点，比如这里的read_email下一个固定是classify_intent。

状态是共享内存，所有节点可见。

当遇到 interrupt() 时，程序会暂停，将所有内容保存到 thread_id 点，然后等待。几天后，程序可以恢复运行，并从上次中断的地方继续执行。thread_id 确保此次会话的所有状态都被完整地保存下来。

thread_id通常用uuid生成。