# LangGraph Learning Notes

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English Version

### About This Project

This project is a hands-on learning repository based on the official LangGraph tutorials, with all LLM calls replaced by Qwen (通义千问) models.

### Introduction

LangGraph is a framework for building stateful, multi-actor applications built on top of LangChain. This project learns how to build complex AI Agent applications through practicing official tutorials.

### Environment Setup

#### Python Version Requirements

Use Python 3.12.11. **DO NOT use version 3.14** as it will cause errors when installing `langgraph-cli[inmem]`.

#### Setup Steps

1. Install Python 3.12.11 using pyenv:
```bash
pyenv install 3.12.11
```

2. Create a virtual environment:
```bash
pyenv virtualenv 3.12.11 langgraph-env
```

3. Set local Python version:
```bash
pyenv local langgraph-env
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Project Structure

```
langgraph-learning/
├── 01_base/              # LangGraph basic examples
├── 02_quickstart/        # Quickstart tutorial
├── 03_thinking_in_langgraph/  # Core LangGraph concepts
└── requirements.txt      # Project dependencies
```

### Tutorials

#### [01_base](01_base/)
Basic LangGraph examples including fundamental graph construction and node definitions.

#### [02_quickstart](02_quickstart/)
Official quickstart tutorial implementation, including:
- Using Qwen model to replace official LLM examples
- Implementing simple Agent loops
- Basic tool calling workflows
- Conditional routing implementation

See [02_quickstart/README.md](02_quickstart/README.md) for details.

#### [03_thinking_in_langgraph](03_thinking_in_langgraph/)
Core LangGraph thinking patterns tutorial, including:
- Breaking workflows into independent steps
- Node and edge design
- State management and sharing
- Dynamic routing and static routing
- Interrupt and resume mechanisms

See [03_thinking_in_langgraph/README.md](03_thinking_in_langgraph/README.md) for details.

### Key Features

- **Using Qwen Model**: All LLM calls use Qwen models through `ChatTongyi` from `langchain-community`
- **Complete State Management**: Managing complex workflows using LangGraph's state graphs
- **Tool Integration**: Demonstrating how to integrate external tools into Agents
- **Interruptible and Resumable**: Supporting interruption and resumption in long-running workflows

### References

- [LangGraph Official Documentation](https://docs.langchain.com/oss/python/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [Qwen API Documentation](https://help.aliyun.com/zh/dashscope/)

### Notes

1. Using Qwen model requires API Key configuration, please refer to Qwen official documentation
2. Python version must be 3.12.x, avoid using 3.14
3. Some tutorials require network access to call Qwen API

---

<a name="中文"></a>
## 中文版本

### 项目简介

本项目是基于 LangGraph 官方教程的学习实践项目，使用通义千问（Qwen）模型替代了原教程中的 LLM 调用。

### 介绍

LangGraph 是一个用于构建有状态、多参与者应用的框架，基于 LangChain 构建。本项目通过实践官方教程，学习如何使用 LangGraph 构建复杂的 AI Agent 应用。

### 环境配置

#### Python 版本要求

使用 Python 3.12.11，**注意不要使用 3.14 版本**，因为在安装 `langgraph-cli[inmem]` 时会报错。

#### 环境搭建步骤

1. 使用 pyenv 安装 Python 3.12.11：
```bash
pyenv install 3.12.11
```

2. 创建虚拟环境：
```bash
pyenv virtualenv 3.12.11 langgraph-env
```

3. 设置本地 Python 版本：
```bash
pyenv local langgraph-env
```

4. 安装依赖包：
```bash
pip install -r requirements.txt
```

### 项目结构

```
langgraph-learning/
├── 01_base/              # LangGraph 基础示例
├── 02_quickstart/        # 快速入门教程
├── 03_thinking_in_langgraph/  # LangGraph 核心思维方式
└── requirements.txt      # 项目依赖
```

### 教程列表

#### [01_base](01_base/)
LangGraph 的基础示例代码，包含基本的图构建和节点定义。

#### [02_quickstart](02_quickstart/)
官方快速入门教程实践，包含：
- 使用 Qwen 模型替代官方示例中的 LLM
- 实现简单的 Agent 循环
- 工具调用的基本流程
- 条件路由的实现

详细说明请查看 [02_quickstart/README.md](02_quickstart/README.md)

#### [03_thinking_in_langgraph](03_thinking_in_langgraph/)
LangGraph 核心思维方式教程，包含：
- 工作流程拆分为独立步骤
- 节点和边的设计
- 状态管理和共享
- 动态路由和静态路由
- 中断和恢复机制

详细说明请查看 [03_thinking_in_langgraph/README.md](03_thinking_in_langgraph/README.md)

### 主要特性

- **使用 Qwen 模型**：所有 LLM 调用都使用通义千问模型，通过 `langchain-community` 的 `ChatTongyi` 实现
- **完整的状态管理**：使用 LangGraph 的状态图管理复杂工作流
- **工具集成**：展示如何将外部工具集成到 Agent 中
- **可中断和恢复**：支持长时间运行的工作流中断和恢复

### 参考资料

- [LangGraph 官方文档](https://docs.langchain.com/oss/python/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [通义千问 API](https://help.aliyun.com/zh/dashscope/)

### 注意事项

1. 使用 Qwen 模型需要配置 API Key，请参考通义千问官方文档
2. Python 版本务必使用 3.12.x，避免使用 3.14
3. 部分教程需要网络访问以调用 Qwen API
