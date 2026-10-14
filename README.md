<div align="center">

# ESP32 iPhone Agent Telegram Bot

**通过 Telegram Bot 远程控制你的 ESP32 iPhone Agent。**

[![CI](https://github.com/your-username/esp32-iphone-agent-telegram-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/esp32-iphone-agent-telegram-bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

> 简体中文 · [English](#english)

## 为什么有这个项目

[ESP32 iPhone Agent](https://github.com/onehumanbeing/esp32-iphone-agent) 是一个极具创新性的项目，它让 AI 模型能够通过一个仅 $7 的 ESP32 板子来控制真实的 iPhone。然而，原项目主要基于局域网内的 Web UI 进行交互，如果你不在同一局域网下，或者希望更便捷地在手机上随时随地下发任务并查看结果，使用体验会受限。

本项目通过封装一个 Telegram Bot，允许你随时随地通过 Telegram 给 Agent 下发指令（如“打开备忘录写一段话”），并自动回传执行过程中的截图和最终结果。它是对主项目生态的一个轻量级补充，不修改主项目核心逻辑，仅作为外部控制端接入。

## 特性

- 💬 **远程指令下发**：通过 Telegram 聊天发送自然语言指令给 iPhone Agent。
- 📸 **截图回传**：自动将 Agent 执行过程中的截图发送回 Telegram 聊天。
- 🔌 **零侵入**：不修改原项目代码，通过调用原项目暴露的 API 接口对接。
- ⚙️ **简单部署**：基于 Python 编写，支持 `pyproject.toml`，几行命令即可启动。

## 安装

1. 确保你已经部署并运行了 [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) 主项目。
2. 在 Telegram 中找 [@BotFather](https://t.me/BotFather) 创建一个 Bot，获取 Token。
3. 克隆本仓库并安装依赖：

```bash
git clone https://github.com/your-username/esp32-iphone-agent-telegram-bot.git
cd esp32-iphone-agent-telegram-bot
pip install -e .
```

## 快速上手

配置环境变量并运行：

```bash
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export AGENT_API_URL="http://localhost:8000" # 主项目 API 地址
python -m esp32_iphone_agent_tg_bot
```

在 Telegram 中给你的 Bot 发送消息：

```
/open Whiteboard and draw a smiley face
```

Bot 将会调用主项目接口执行任务，并实时回复截图。

## 与主项目的关系

本项目是一个基于 [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) 的二创生态项目。主项目负责底层的硬件控制、屏幕镜像和 AI 模型对接，本项目仅提供一个 Telegram 的远程控制端封装。你需要先运行主项目才能使用本项目。

## Roadmap

- [x] 基础指令下发与结果回传
- [x] 多用户鉴权
- [ ] 支持流式回复执行过程
- [ ] 支持语音输入指令

## License

[MIT](LICENSE) © 2024

---

<a id="english"></a>

<div align="center">

# ESP32 iPhone Agent Telegram Bot (English)

**Control your ESP32 iPhone Agent remotely via Telegram bot.**

</div>

## Why this project

[ESP32 iPhone Agent](https://github.com/onehumanbeing/esp32-iphone-agent) is a highly innovative project that allows AI models to control a real iPhone through a $7 ESP32 board. However, the original project relies on a web UI accessible primarily over a local network. If you are not on the same network or want to easily send tasks and check results on the go from your phone, the experience is limited.

This project wraps a Telegram Bot, allowing you to send natural language commands to the Agent (e.g., "Open Notes and write a paragraph") anytime, anywhere via Telegram, and automatically sends back screenshots and final results. It is a lightweight addition to the main project's ecosystem, not modifying the core logic, just acting as an external control endpoint.

## Features

- 💬 **Remote Command Dispatch**: Send natural language commands to the iPhone Agent via Telegram chat.
- 📸 **Screenshot Feedback**: Automatically sends back screenshots taken during the Agent's execution to the Telegram chat.
- 🔌 **Non-intrusive**: Does not modify the original project code, integrates by calling the original project's exposed API.
- ⚙️ **Easy Deployment**: Written in Python, uses `pyproject.toml`, starts with just a few commands.

## Installation

1. Ensure you have deployed and are running the [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent) main project.
2. Talk to [@BotFather](https://t.me/BotFather) on Telegram to create a Bot and get the Token.
3. Clone this repo and install dependencies:

```bash
git clone https://github.com/your-username/esp32-iphone-agent-telegram-bot.git
cd esp32-iphone-agent-telegram-bot
pip install -e .
```

## Quick Start

Set environment variables and run:

```bash
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export AGENT_API_URL="http://localhost:8000" # Main project API URL
python -m esp32_iphone_agent_tg_bot
```

Send a message to your bot in Telegram:

```
/open Whiteboard and draw a smiley face
```

The bot will call the main project API to execute the task and reply with screenshots in real-time.

## Relationship to the main project

This project is a derivative ecosystem project based on [esp32-iphone-agent](https://github.com/onehumanbeing/esp32-iphone-agent). The main project handles underlying hardware control, screen mirroring, and AI model integration. This project simply provides a Telegram remote control wrapper. You must run the main project to use this project.

## Roadmap

- [x] Basic command dispatch and result feedback
- [x] Multi-user authentication
- [ ] Support streaming replies for execution progress
- [ ] Support voice input commands

## License

[MIT](LICENSE) © 2024