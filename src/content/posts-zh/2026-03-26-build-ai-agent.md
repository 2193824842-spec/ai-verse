---
title: "用 Claude 4.6 API 构建你的第一个多步骤 AI Agent"
date: 2026-03-26
difficulty: 中级
summary: "通过 Anthropic Python SDK，手把手实现一个能自主拆解任务、调用工具、循环执行的 AI Agent，体验 2026 年最火的智能体开发范式。"
cover: "/ai-blog/covers/2026-03-26-build-ai-agent.png"
tags: ["AI Agent", "Claude 4.6", "AI教程", "Python", "大模型"]
---

## 引言

2026 年，AI 领域最热的词不是"大模型"，而是 **AI Agent**。

从 GitHub 最热项目 OpenClaw，到亚马逊推出的 Health AI 智能体，再到 Claude Code 的多智能体并行编程——"聊天工具"正在进化为"能干事的自主系统"。

本教程将带你用 **Claude 4.6 API + Python**，从零构建一个真正能运行的多步骤 AI Agent。

## 环境准备

```bash
# Python 3.10+
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxx"
```

## 核心概念：什么是 Agentic Loop？

```
用户输入
  ↓
Claude 思考 → 需要工具？
  ├── 是 → 调用工具 → 拿到结果 → 返回 Claude → 继续思考
  └── 否 → 输出最终答案
```

这个"思考-调用-反馈"的循环就是 **Agentic Loop**，也是 Agent 区别于普通聊天的核心。

## 实战：Tool Runner（推荐方式）

```python
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

# 1. 用装饰器定义工具
@beta_tool
def calculator(expression: str) -> str:
    """安全地计算数学表达式。

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"

# 2. Tool Runner 自动处理循环
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=4096,
    tools=[calculator],
    messages=[{"role": "user", "content": "帮我计算：(123 + 456) * 789 是多少？"}],
)

# 3. 迭代结果
for message in runner:
    for block in message.content:
        if block.type == "text":
            print(block.text)
```

## 实战：手动 Agentic Loop（理解底层原理）

```python
import anthropic

client = anthropic.Anthropic()

tools = [{
    "name": "search_web",
    "description": "搜索网络上的最新信息",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    }
}]

messages = [{"role": "user", "content": "2026年3月 AI 领域有哪些重大进展？"}]

while True:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )

    # Agent 完成，退出循环
    if response.stop_reason == "end_turn":
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    # Agent 请求工具
    messages.append({"role": "assistant", "content": response.content})

    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            # 模拟工具执行
            result = f"搜索到关于 '{block.input['query']}' 的结果：Claude 4.6 发布，支持百万 token 上下文..."
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

    messages.append({"role": "user", "content": tool_results})
```

## 运行效果

```
> python agent.py
[调用工具] search_web("2026年3月 AI 进展")
[工具结果] 搜索到关于 '2026年3月 AI 进展' 的结果...

根据搜索结果，2026年3月 AI 领域的重大进展包括：

1. **Claude Opus 4.6 发布** — 支持百万 token 上下文...
2. **Gemini 3.1 Pro** — 在 13 项基准测试中领先...
3. **GPT-5.4** — 原生计算机控制能力...
```

## 进阶方向

- **多 Agent 协作**：Claude Code 的并行多智能体架构
- **持久化记忆**：Memory Tool + 文件系统
- **MCP 集成**：连接外部数据库、浏览器、代码执行环境
- **流式输出**：用 `.stream()` 实现实时打字效果

## 总结

| 方式 | 适合场景 | 代码量 |
|------|---------|--------|
| Tool Runner | 快速原型、生产环境 | 少 |
| 手动 Loop | 学习原理、自定义控制流 | 多 |

Agent 时代已经到来。现在是上手的最好时机。
