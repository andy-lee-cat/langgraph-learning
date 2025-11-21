# Streaming

## intro

流式传输，1️⃣逐步显示2️⃣llm的流式传输

官方教程：[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)

## 流式传输的模式

- values: 显示状态的值
- updates：图毎执行一步会更新values，显示有哪些变量更新了
- custom: 图节点内部自定义传输数据
- messages: 调用llm的任何图节点流式返回2元组(llm token, metadata)
- debug: 基本所有额外信息

### 基本用法

```python
for chunk in graph.stream(inputs, stream_mode="updates"):
    print(chunk)
```

参考示例 [流式模式](stream_updates.ipynb)

### 流图状态

使用updates和values来流式传输图的状态。

参考示例：[流图状态](stream_graph_state.ipynb)

### 子图输出

```python
for chunk in graph.stream(
    {"foo": "foo"},
    # Set subgraphs=True to stream outputs from subgraphs
    subgraphs=True,  
    stream_mode="updates",
):
    print(chunk)
```

### debug模式

debug模式就是会输出几乎所有信息。

## llm token

逐token进行输出。输出单位是元组(message_chunk, metadata)。[示例](stream_llm.ipynb)

而且可以在init_model时指定tag，输出时按照tag决定是否输出。[示例](stream_llm_tag.ipynb)

也可以按照节点筛选。[示例](stream_llm_node.ipynb)

```python
for msg, metadata in graph.stream(
    inputs,
    stream_mode="messages",
):
    if msg.content and metadata["langgraph_node"] == "some_node_name":
        ...
```

## 流式自定义数据

使用get_stream_writer()发出自定义数据。[示例](stream_custom_data.ipynb)
