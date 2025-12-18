# LangGraph 新项目模版

[![CI](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml)

这个模版展示了一个使用 [LangGraph](https://github.com/langchain-ai/langgraph) 实现的简单应用，旨在演示如何开始使用 [LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/#langgraph-server) 以及 [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)（一个可视化调试 IDE）。

<div align="center">
  <img src="./static/studio_ui.png" alt="LangGraph Studio UI 中的图形视图" width="75%" />
</div>

核心逻辑定义在 `src/agent/graph.py` 中，展示了一个单步应用，它会返回一个固定字符串和提供的配置信息。

你可以扩展这个图形来编排更复杂的智能代理工作流，这些工作流可以在 LangGraph Studio 中进行可视化和调试。

## 快速开始

1. 安装依赖，以及用于运行服务器的 [LangGraph CLI](https://langchain-ai.github.io/langgraph/concepts/langgraph_cli/)。

```bash
cd path/to/your/app
pip install -e . "langgraph-cli[inmem]"
```

2. （可选）根据需要自定义代码和项目。如果需要使用密钥，请创建 `.env` 文件。

```bash
cp .env.example .env
```

如果你想启用 LangSmith 追踪，请将你的 LangSmith API 密钥添加到 `.env` 文件中。

```text
# .env
LANGSMITH_API_KEY=lsv2...
```

3. 启动 LangGraph 服务器。

```shell
langgraph dev
```

有关 LangGraph 服务器入门的更多信息，[请参阅这里](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)。

## 如何自定义

1. **定义运行时上下文**：修改 `graph.py` 文件中的 `Context` 类，以暴露你想要为每个助手配置的参数。例如，在聊天机器人应用中，你可能想要定义动态的系统提示词或要使用的 LLM。有关 LangGraph 中运行时上下文的更多信息，[请参阅这里](https://langchain-ai.github.io/langgraph/agents/context/?h=context#static-runtime-context)。

2. **扩展图形**：应用的核心逻辑定义在 [graph.py](./src/agent/graph.py) 中。你可以修改此文件来添加新节点、边，或更改信息流。

## 开发

在 LangGraph Studio 中迭代你的图形时，你可以编辑过去的状态并从之前的状态重新运行应用以调试特定节点。本地更改将通过热重载自动应用。

后续请求会扩展同一个线程。你可以使用右上角的 `+` 按钮创建一个全新的线程，清除之前的历史记录。

更多高级功能和示例，请参阅 [LangGraph 文档](https://langchain-ai.github.io/langgraph/)。这些资源可以帮助你根据特定用例调整此模版，并构建更复杂的对话代理。

LangGraph Studio 还集成了 [LangSmith](https://smith.langchain.com/)，用于更深入的追踪和与团队成员的协作，使你能够分析和优化聊天机器人的性能。

---

# 配置文件详解

## 一、GitHub Actions 工作流 YAML 文件详解

### 1. 单元测试工作流 (unit-tests.yml)

```yaml
# 此工作流将为当前项目运行单元测试
# 这是一行注释，说明此工作流的用途

name: CI
# 工作流的名称，显示在 GitHub Actions 界面中

on:
# 定义触发此工作流的事件
  push:
  # 当有代码推送时触发
    branches: ["main"]
    # 仅在推送到 "main" 分支时触发
  pull_request:
  # 当创建或更新 Pull Request 时触发（任何分支）
  workflow_dispatch:
  # 允许在 GitHub UI 中手动触发此工作流

# 如果在此工作流仍在运行时，又有新的推送到同一 PR 或分支，
# 则取消之前的运行，优先执行新的运行。
concurrency:
# 并发控制配置
  group: ${{ github.workflow }}-${{ github.ref }}
  # 并发组名称，由工作流名称和分支引用组成
  # 同一组内的工作流运行会互相影响
  cancel-in-progress: true
  # 设置为 true 表示取消正在进行的旧运行

jobs:
# 定义工作流中的任务
  unit-tests:
  # 任务 ID
    name: Unit Tests
    # 任务显示名称
    strategy:
    # 策略配置，用于矩阵构建
      matrix:
      # 矩阵配置，会创建多个并行任务
        os: [ubuntu-latest]
        # 操作系统列表
        python-version: ["3.11", "3.12"]
        # Python 版本列表
        # 这会创建 1(os) × 2(python) = 2 个并行任务
    runs-on: ${{ matrix.os }}
    # 指定运行环境，使用矩阵中的操作系统
    steps:
    # 任务步骤列表
      - uses: actions/checkout@v4
      # 检出代码仓库，使用官方 checkout action v4 版本

      - name: Set up Python ${{ matrix.python-version }}
      # 步骤名称，显示当前设置的 Python 版本
        uses: actions/setup-python@v4
        # 使用官方 setup-python action v4 版本
        with:
        # action 的输入参数
          python-version: ${{ matrix.python-version }}
          # 指定要安装的 Python 版本

      - name: Install dependencies
      # 安装依赖步骤
        run: |
        # 运行 shell 命令，| 表示多行命令
          curl -LsSf https://astral.sh/uv/install.sh | sh
          # 下载并安装 uv 包管理器
          # -L: 跟随重定向  -s: 静默模式  -S: 显示错误  -f: 失败时静默
          uv venv
          # 使用 uv 创建虚拟环境
          uv pip install -r pyproject.toml
          # 从 pyproject.toml 安装项目依赖

      - name: Lint with ruff
      # 使用 ruff 进行代码检查
        run: |
          uv pip install ruff
          # 安装 ruff 代码检查工具
          uv run ruff check .
          # 在虚拟环境中运行 ruff 检查当前目录所有文件

      - name: Lint with mypy
      # 使用 mypy 进行类型检查
        run: |
          uv pip install mypy
          # 安装 mypy 类型检查工具
          uv run mypy --strict src/
          # 以严格模式检查 src/ 目录的类型注解

      - name: Check README spelling
      # 检查 README 文件的拼写
        uses: codespell-project/actions-codespell@v2
        # 使用 codespell action 进行拼写检查
        with:
          ignore_words_file: .codespellignore
          # 指定忽略词文件
          path: README.md
          # 仅检查 README.md 文件

      - name: Check code spelling
      # 检查代码文件的拼写
        uses: codespell-project/actions-codespell@v2
        with:
          ignore_words_file: .codespellignore
          path: src/
          # 检查 src/ 目录下的所有文件

      - name: Run tests with pytest
      # 使用 pytest 运行测试
        run: |
          uv pip install pytest
          # 安装 pytest 测试框架
          uv run pytest tests/unit_tests
          # 运行 tests/unit_tests 目录下的单元测试
```

### 2. 集成测试工作流 (integration-tests.yml)

```yaml
# 此工作流将每天为当前项目运行一次集成测试
# 集成测试通常需要外部服务（如 API），所以不在每次提交时运行

name: Integration Tests
# 工作流名称

on:
# 触发事件
  schedule:
  # 定时触发
    - cron: "37 14 * * *"
    # cron 表达式：分 时 日 月 周
    # "37 14 * * *" = 每天 UTC 时间 14:37 运行（太平洋时间 7:37 AM）
    # 使用非整点时间以避免与其他任务冲突
  workflow_dispatch:
  # 允许手动触发

# 如果在此工作流仍在运行时开始另一个计划运行，
# 则取消之前的运行，优先执行新的运行。
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  integration-tests:
    name: Integration Tests
    strategy:
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.11", "3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          uv venv
          uv pip install -r pyproject.toml
          uv pip install -U pytest-asyncio
          # 额外安装 pytest-asyncio 用于异步测试支持
          # -U 表示升级到最新版本

      - name: Run integration tests
      # 运行集成测试
        env:
        # 设置环境变量（从 GitHub Secrets 获取）
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          # Anthropic API 密钥
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
          # LangSmith API 密钥
          LANGSMITH_TRACING: true
          # 启用 LangSmith 追踪
        run: |
          uv run pytest tests/integration_tests
          # 运行 tests/integration_tests 目录下的集成测试
```

---

## 二、pyproject.toml 配置文件详解

```toml
[project]
name = "agent"                    # 项目名称
version = "0.0.1"                 # 版本号
description = "Starter template for making a new agent LangGraph."  # 项目描述
authors = [                       # 作者信息
    { name = "William Fu-Hinthorn", email = "13333726+hinthornw@users.noreply.github.com" },
]
readme = "README.md"              # README 文件路径
license = { text = "MIT" }        # 开源许可证
requires-python = ">=3.10"        # 要求 Python 3.10 或更高版本

dependencies = [                  # 项目核心依赖
    "langgraph>=1.0.0",           # LangGraph 框架
    "python-dotenv>=1.0.1",       # 用于加载 .env 文件的环境变量
]

[project.optional-dependencies]   # 可选依赖组
dev = [                           # 开发依赖
    "mypy>=1.11.1",               # 类型检查工具
    "ruff>=0.6.1"                 # 代码检查和格式化工具
]

[build-system]                    # 构建系统配置
requires = ["setuptools>=73.0.0", "wheel"]  # 构建所需的包
build-backend = "setuptools.build_meta"     # 使用 setuptools 作为构建后端

[tool.setuptools]                 # setuptools 特定配置
packages = ["langgraph.templates.agent", "agent"]  # 要打包的模块

[tool.setuptools.package-dir]     # 包目录映射
"langgraph.templates.agent" = "src/agent"  # 命名空间包
"agent" = "src/agent"             # 简短包名

[tool.setuptools.package-data]    # 包数据文件
"*" = ["py.typed"]                # 包含类型标记文件

[tool.ruff]                       # ruff 代码检查配置
lint.select = [                   # 启用的检查规则
    "E",     # pycodestyle 错误
    "F",     # pyflakes 错误
    "I",     # isort 导入排序
    "D",     # pydocstyle 文档字符串
    "D401", # 首行应使用祈使句
    "T201",  # print 语句检查
    "UP",    # pyupgrade 现代化语法
]
lint.ignore = [                   # 忽略的规则
    "UP006", "UP007", "UP035",    # 某些 typing 升级规则
    "D417",  # 不要求每个参数都有文档
    "E501",  # 行长度限制（允许长行）
]

[tool.ruff.lint.per-file-ignores] # 按文件忽略规则
"tests/*" = ["D", "UP"]           # 测试文件忽略文档和升级规则

[tool.ruff.lint.pydocstyle]       # pydocstyle 配置
convention = "google"             # 使用 Google 风格的文档字符串

[dependency-groups]               # uv 的依赖组功能
dev = [                           # 开发组依赖
    "anyio>=4.7.0",               # 异步 I/O 库
    "langgraph-cli[inmem]>=0.4.7", # LangGraph CLI（带内存存储）
    "mypy>=1.13.0",               # 类型检查
    "pytest>=8.3.5",              # 测试框架
    "ruff>=0.8.2",                # 代码检查
]
```

---

## 三、langgraph.json 配置文件详解

```json
{
  "$schema": "https://langgra.ph/schema.json",  // JSON Schema 验证地址
  "dependencies": ["."],                         // 依赖项，"." 表示当前项目
  "graphs": {                                    // 图形定义
    "agent": "./src/agent/graph.py:graph"        // "agent" 图形的路径和对象名
  },
  "env": ".env",                                 // 环境变量文件路径
  "image_distro": "wolfi"                        // Docker 镜像基础发行版
}
```

---

## 四、uv.lock 文件说明

`uv.lock` 是 [uv](https://github.com/astral-sh/uv) 包管理器生成的锁定文件，它锁定了项目所有依赖的精确版本，确保在不同环境中安装完全相同的依赖版本。

主要内容：
- **version**: 锁定文件格式版本
- **requires-python**: Python 版本要求 (>=3.10)
- **resolution-markers**: 不同 Python 版本的解析标记
- **[[package]]**: 每个依赖包的详细信息，包括：
  - `name`: 包名
  - `version`: 精确版本号
  - `source`: 包来源（如 PyPI）
  - `dependencies`: 该包的依赖
  - `sdist`/`wheels`: 包的下载地址和哈希值

---

## 五、常用指令汇总

### 1. 项目初始化和依赖安装

```bash
# 方式一：使用 pip
pip install -e . "langgraph-cli[inmem]"

# 方式二：使用 uv（推荐，更快）
uv venv                           # 创建虚拟环境
uv pip install -r pyproject.toml  # 安装依赖
uv pip install -e .               # 以可编辑模式安装项目

# 安装开发依赖
uv pip install -e ".[dev]"
```

### 2. 启动 LangGraph 服务器

```bash
langgraph dev                     # 启动开发服务器（支持热重载）
```

### 3. 测试相关指令 (Makefile)

```bash
make test                         # 运行单元测试
make test TEST_FILE=tests/xxx     # 运行指定测试文件
make integration_tests            # 运行集成测试
make test_watch                   # 监视模式运行测试（文件变化自动重测）
make test_profile                 # 运行测试并生成性能分析报告
```

### 4. 代码检查和格式化 (Makefile)

```bash
make lint                         # 运行所有代码检查（ruff + mypy）
make format                       # 格式化代码
make lint_diff                    # 仅检查相对于 main 分支的更改
make spell_check                  # 拼写检查
make spell_fix                    # 自动修复拼写错误
```

### 5. 使用 uv 直接运行

```bash
uv run pytest tests/unit_tests    # 在虚拟环境中运行 pytest
uv run ruff check .               # 在虚拟环境中运行 ruff
uv run mypy --strict src/         # 在虚拟环境中运行 mypy
```

### 6. 查看帮助

```bash
make help                         # 显示所有可用的 make 命令
```

---

## 六、项目结构说明

```
03_template/
├── .github/
│   └── workflows/
│       ├── integration-tests.yml  # 集成测试工作流
│       └── unit-tests.yml         # 单元测试工作流
├── src/
│   └── agent/
│       └── graph.py               # 核心图形逻辑
├── tests/
│   ├── unit_tests/                # 单元测试
│   └── integration_tests/         # 集成测试
├── static/                        # 静态资源
├── .env.example                   # 环境变量示例
├── .gitignore                     # Git 忽略文件
├── langgraph.json                 # LangGraph 配置
├── Makefile                       # 构建和测试脚本
├── pyproject.toml                 # 项目配置和依赖
├── uv.lock                        # 依赖锁定文件
└── README.md                      # 项目说明文档
```
