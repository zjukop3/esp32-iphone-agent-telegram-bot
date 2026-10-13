<div align="center">

# ESP32 iPhone Agent Telegram Bot

**通过 Telegram 远程控制 ESP32 操控的 iPhone。**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots/api)

</div>

> **简体中文** · [English](#english)

## 为什么有这个项目？

[esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) 是一个极具创新性的项目，它让 AI 模型能够通过一个仅 $7 的 ESP32 开发板来操控真实的 iPhone，无需 Mac、无需开发者账号、无需越狱。

但原项目的交互方式主要依赖于本地 Web UI，这限制了它的使用场景：你必须在同一局域网内才能下达指令。为了拓展它的使用边界，我开发了本附属项目。`esp32-iphone-agent-telegram-bot` 封装了一个 Telegram Bot，允许你随时随地通过 Telegram 向 ESP32 操控的 iPhone 下发任务指令，并自动回传执行过程的截图与结果。

## 特性

- 🤖 **远程指令下发**：通过 Telegram 文本消息直接发送自然语言任务。
- 🖼️ **截图回传**：任务执行过程中的关键截图自动发送至 Telegram 聊天。
- 🔄 **异步执行**：不阻塞 Telegram 消息接收，任务在后台队列执行并反馈状态。
- 📝 **状态追踪**：自动反馈任务状态（已接收、执行中、成功、失败）。

## 安装

本项目依赖于 `esp32-iphone-agent` 的核心运行环境，请确保你已经按照[原项目教程](https://github.com/onehumanbeing/esp32-iphone-agent)完成了硬件搭建和基础环境配置。

1. **克隆本仓库**

```bash
git clone https://github.com/zjukop3/esp32-iphone-agent-telegram-bot.git
cd esp32-iphone-agent-telegram-bot
```

2. **安装依赖**

```bash
pip install -e .
```

3. **配置环境变量**

创建 `.env` 文件：

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
AGENT_API_URL=http://localhost:8000 # esp32-iphone-agent 的 API 地址
```

## 快速上手

1. 启动 `esp32-iphone-agent` 主服务。
2. 运行 Telegram Bot：

```bash
python -m esp32_iphone_agent_telegram_bot.main
```

3. 在 Telegram 中找到你的 Bot，发送指令：

```text
/open Whiteboard and draw a smiley face
```

Bot 将回复任务已接收，并在执行完成后回传 iPhone 屏幕的截图。

## 与主项目的关系

这是一个**非官方的生态补充项目**。本项目不包含任何原项目的核心代码，仅通过 HTTP API 与 `esp32-iphone-agent` 服务进行交互。所有关于 iPhone 硬件控制、AirPlay 屏幕镜像、视觉模型调度的核心能力均由[原项目](https://github.com/onehumanbeing/esp32-iphone-agent)提供。本项目旨在为原项目提供一种便捷的远程控制方案，绝不抢夺主项目定位。

## Roadmap

- [x] 基础指令接收与转发
- [x] 执行结果截图回传
- [ ] 支持多任务队列管理
- [ ] 支持任务执行过程流式截图回传
- [ ] Telegram Inline Keyboard 快捷指令

## License

[MIT](LICENSE)

---

## English

A Telegram bot bridge for [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent). Send natural language tasks via Telegram to the ESP32-controlled iPhone and receive execution screenshots back.

### Why this project?

The original project relies on a local Web UI, meaning you have to be on the same network to give instructions. This companion repo wraps a Telegram Bot around the agent, allowing you to send tasks from anywhere and get visual feedback directly in your Telegram chat.

### Features

- Remote task dispatch via Telegram text messages.
- Automatic screenshot feedback of execution results.
- Asynchronous execution with status updates.

### Installation

1. Ensure you have set up the [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) environment.
2. Clone this repo and install dependencies:

```bash
pip install -e .
```

3. Configure `.env` with your `TELEGRAM_BOT_TOKEN` and `AGENT_API_URL`.

### Quick Start

Run the bot:

```bash
python -m esp32_iphone_agent_telegram_bot.main
```

Send a message to your bot:

```text
/open Whiteboard and draw a smiley face
```

### Relationship to the main project

This is an **unofficial companion project**. It does not contain core code from the original repo. It interacts with the `esp32-iphone-agent` service purely via HTTP API. All hardware control and vision model capabilities are provided by the [main project](https://github.com/onehumanbeing/esp32-iphone-agent).