# Subgraphs

## intro

相关的许多例子在 03_streaming/ 里面提到过。

子图的用途与优势：

- 构建 multi-agent systems
- 多个图中重用一个节点
- 分布式开发，每个团队独立处理图的不同部分

子图如何使用：

- 从节点调用图，在节点的逻辑内部调用子图逻辑
- 将子图添加为一个节点，与父节点共享状态

官方文档：[Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs#stream-from-subgraphs)

## 子图的两种使用方式

[节点调用图](invoke_graph_from_node.ipynb)

[子图添加为节点](graph_ad_node.ipynb)

## 子图的持久化

只需要在编译父图时提供检查点，langgraph会把检查点传播给子图。

```python
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

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

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

如果希望子图拥有自己的内存，可以使用相应的检查点选项进行编译。多智能体系统中经常用到。

```python
subgraph_builder = StateGraph(...)
subgraph = subgraph_builder.compile(checkpointer=True)
```

## 查看子图的state

通过`graph.get_state(config)`查看图的状态。通过`graph.get_state(config, subgraphs=True)`查看子图的状态（当且仅当子图被中断时）。

## 子图流式输出

```python
for chunk in graph.stream(
    {"foo": "foo"},
    subgraphs=True, 
    stream_mode="updates",
):
    print(chunk)
```
