# Memory

## intro

AI应用需要记忆来跨多个交互来共享上下文，在langgraph中有两种memroy：

- 将短期记忆（线程持久化）添加到代理的状态中，以支持多轮对话
- 长期记忆来存储跨会话或应用程序级的数据

详细文档：[Memory](https://docs.langchain.com/oss/python/langgraph/add-memory#example-using-postgres-checkpointer)

## 短期记忆

### Inmemory

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

checkpointer = InMemorySaver()

builder = StateGraph(...)
graph = builder.compile(checkpointer=checkpointer)

graph.invoke(
    {"message": [{"role": "user", "content": "hi! I am Alice."}]},
    {"configrable": {"thread_id": "1"}}
)
```

### production生产环境

安装对应的库，详细看官方文档

下面的例子是Postgres数据库的，MongoDB和Redis都是类似的

```python
# sync
from langgraph.checkpoint.postgres import PostgresSaver
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    ...

# async
from langgraph.checkpoint.postgres.aio import PostgresSaver
async with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    ...
```

### 子图记忆

```python
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict

class State(TypedDict):
    foo: str

# Subgraph

def subgraph_node_1(state: State):
    return {"foo": state["foo"] + "bar"}

subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()  

# Parent graph

builder = StateGraph(State)
builder.add_node("node_1", subgraph)  
builder.add_edge(START, "node_1")

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

上面是一个基本的子图示例，如果想要子图有记忆，修改下面这行

```python
subgraph_builder = StateGraph(...)
subgraph = subgraph_builder.compile(checkpointer=True)  # 这里修改为True
```

## 长期记忆

用store。

第一次使用 Postgres store 时你需要调用 store.setup()

```python
from langgraph.store.memory import InMemoryStore  
from langgraph.graph import StateGraph

store = InMemoryStore()  

builder = StateGraph(...)
graph = builder.compile(store=store)
```

```python
# ... (来自你之前发的长文档 Prompt 4)
DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"

with (
    PostgresStore.from_conn_string(DB_URI) as store,
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
):
    # store.setup()          <-- 我指的是这里
    # checkpointer.setup()   <-- 还有这里
```


## 语义搜索

可以参考[memory_stroe](../01_persistence/memory_store.ipynb)

## 管理短期记忆

有可能超出llm的上下文窗口，常见解决方案有：

- 裁剪消息：移除前N条信息或后N条信息
- 永久删除Langgraph状态中的信息
- 信息摘要
- 管理检查点
- 自定义策略（如消息过滤等）

详细内容查看[manage_memory](manage_memory.ipynb)

裁剪信息用到了langmem库，也是langchain维护的一个库，提供了一些用于管理代理中长期记忆的工具。