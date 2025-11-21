# Interrupts

## intro

中断允许在特定点暂停图的运行，等待外部输入后再继续。interrupt()函数中断，接受任何可序列化的JSON值。Command来恢复执行，该值为节点ininterrupt()调用的返回值。

文档：[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## 使用interrupt暂停

```python
from langgraph.types import interrupt

def approval_node(state: State):
    # Pause and ask for approval
    approved = interrupt("Do you approve this action?")

    # when you resume, Command(resume=...) returns that value here
    return {"approved": approved}
```

## 典型场景

### approve or reject

参考示例 [approve or reject](approve_reject.ipynb)

```python
from typing import Literal
from langgraph.types import interrupt, Command

def approval_node(state: State) -> Command[Literal["proceed", "cancel"]]:
    # Pause execution; payload shows up under result["__interrupt__"]
    is_approved = interrupt({
        "question": "Do you want to proceed with this action?",
        "details": state["action_details"]
    })

    # Route based on the response
    if is_approved:
        return Command(goto="proceed")  # Runs after the resume payload is provided
    else:
        return Command(goto="cancel")
```

### review and edit state

参考示例：[review and edit state](review_edit.ipynb)

```python
from langgraph.types import interrupt

def review_node(state: State):
    # Pause and show the current content for review (surfaces in result["__interrupt__"])
    edited_content = interrupt({
        "instruction": "Review and edit this content",
        "content": state["generated_text"]
    })

    # Update the state with the edited version
    return {"generated_text": edited_content}
```

### interrupte tools

工具里加中断，一样的实现方式。

### 验证人工输入（多次验证）

一个while循环，验证输入，直到输入正确为止。

```python
from langgraph.types import interrupt

def get_age_node(state: State):
    prompt = "What is your age?"

    while True:
        answer = interrupt(prompt)  # payload surfaces in result["__interrupt__"]

        # Validate the input
        if isinstance(answer, int) and answer > 0:
            # Valid input - continue
            break
        else:
            # Invalid input - ask again with a more specific prompt
            prompt = f"'{answer}' is not a valid age. Please enter a positive number."

    return {"age": answer}
```

## 一些规则

- 不要讲interrupt包装在try/except里面，因为interrupt的实现是基于特殊异常的
- 多个interrupt的顺序不要修改，不然重新恢复会出错（按照索引匹配的）
- 不要返回复杂结果，返回简单的可序列化的JSON类型
- interrupt之前的调用必须是幂等的，创建记录前先检查是否存在，尽可能将副作用分离到单独节点

## 中断用于debug

at compile time

```python
graph = builder.compile(
    interrupt_before=["node_a"],  
    interrupt_after=["node_b", "node_c"],  
    checkpointer=checkpointer,
)

# Pass a thread ID to the graph
config = {
    "configurable": {
        "thread_id": "some_thread"
    }
}

# Run the graph until the breakpoint
graph.invoke(inputs, config=config)  

# Resume the graph
graph.invoke(None, config=config)
```

at run time

```python
config = {
    "configurable": {
        "thread_id": "some_thread"
    }
}

# Run the graph until the breakpoint
graph.invoke(
    inputs,
    interrupt_before=["node_a"],  
    interrupt_after=["node_b", "node_c"],  
    config=config,
)

# Resume the graph
graph.invoke(None, config=config)
```