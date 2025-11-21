# Persistence

## Threads

检查点的唯一标识符，状态会持久化到该thread中。使用检查点调用图时必须指定threads。`{"configurable": {"threads": "1"}}`

## checkpoint

线程在特定时间到状态称为检查点checkpoint，状态快照，表示为对象`StateSnapshot`。

## memory store

对比checkpoint的config是在相同thread中的状态，我们在不同对话thread间也想保存一些信息。这就需要用到Store接口。

## 如何在langgraph中运用

这里举了一个例子，没对着敲代码。简单来说就是可以通过update_memory来更新store中的数据，在不同的图thread中都可以进行访问。