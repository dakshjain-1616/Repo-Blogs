---
title: "Stock Trading Agent Swarm: How NEO Coordinated 10 Specialized Agents on a Simulated Portfolio"
description: "NEO built a multi-agent trading simulation with 10 specialized agents coordinating over an async message bus, achieving +4.62% returns across 250 days of S&P 500 data with an 86.9% order approval rate."
date: 2026-03-09
tags: [multi-agent systems, trading simulation, agent swarm, async messaging, Python, financial AI]
slug: stock-trading-agent-swarm
github: https://github.com/dakshjain-1616/Stock-trading-Agent-Swarm
---

# Stock Trading Agent Swarm: How NEO Coordinated 10 Specialized Agents on a Simulated Portfolio

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/Stock-trading-Agent-Swarm)

![Pipeline Architecture](../public/images/diagrams/stock-trading-agent-swarm.png)

## The Problem

> Multi-agent systems are easy to talk about and hard to actually build. Coordination overhead, message ordering, deadlocks, agents that step on each other's decisions — most implementations that look clean in architecture diagrams get messy fast when you wire them together. The challenge isn't any single piece; it's building coordination patterns that stay coherent as agents multiply and interact under real conditions.

NEO autonomously built a 10-agent trading simulation to work through these problems in a domain that makes the coordination challenges concrete. Ten specialized agents, an asynchronous message bus, $1M in simulated capital, and 250 days of real S&P 500 data to test against. The result was **+4.62% returns**, **86 executed trades**, and a system that blocked **26 risky positions** before they went through.

This is an educational simulation, not trading advice. But the engineering is real.

## The Agent Architecture

The system divides work across four distinct roles, each handled by dedicated agents.

### Analyst Agents (3 agents)

The analyst agents generate trade signals using technical indicators. They monitor price data, compute indicator values, and publish signals to the message bus when conditions suggest a position worth taking. Three analysts running in parallel means multiple indicator strategies can run simultaneously, and their signals can be aggregated or compared by downstream agents.

No analyst agent executes trades directly. Their job is signal generation only. This separation of concerns keeps the analysis layer from being coupled to risk or execution logic.

### Trader Agents (4 agents)

Trader agents subscribe to signals from the analyst layer and manage individual portfolios. They receive a signal, determine position sizing, and submit orders. But they do not have unilateral authority to execute. Every order goes through risk validation before it reaches the market simulation.

Four trader agents each managing a portion of the capital creates natural diversification within the simulation and lets you observe how different traders respond to the same signal.

### Risk Manager Agents (2 agents)

Risk managers validate every order before it executes. They enforce position limits, check stop-loss rules, and can block trades that violate the configured risk parameters. In the 250-day simulation, risk managers blocked 26 risky positions and triggered 20 stop-losses.

The stop-loss enforcement is particularly important. An agent system without hard risk controls can run up losses on a bad position indefinitely. The risk layer enforces discipline that individual trader agents might not.

### Reporter Agent (1 agent)

The reporter aggregates metrics across all agents and produces performance summaries. Trade count, returns, approval rates, blocked orders. This is the observability layer for the whole system.

## The Message Bus

All coordination happens through an in-memory publish/subscribe message bus. Agents do not call each other directly. An analyst publishes a signal. Trader agents subscribed to that signal receive it. Traders submit orders. Risk managers subscribed to the order topic validate them.

Asynchronous message passing is what makes the architecture scale. Agents operate independently. No agent blocks waiting for another to respond. The bus handles delivery and ordering.

This design also makes the system extensible. Adding a new agent type means subscribing to the relevant topics and publishing to the appropriate output topics. You do not need to modify existing agents.

## Simulation Results

On **$1M** in simulated capital across **250 days** of S&P 500 data:

- **Total return: +4.62%**
- **Executed trades: 86**
- **Order approval rate: 86.9%**
- **Positions blocked by risk managers: 26**
- **Stop-losses triggered: 20**

The 86.9% approval rate tells you that the risk layer is active and filtering, not rubber-stamping orders. 13% of submitted orders were rejected, which reflects real risk management behavior rather than a system that passes everything through.

## Technical Stack

Python 3.12, Pydantic for message schema validation, yfinance for historical S&P 500 data, and Docker for containerized deployment. The Pydantic schemas are important. When agents communicate through a message bus, message schemas are your contract. Strict typing at the message level catches coordination bugs early.

Docker Compose handles multi-container deployment so the full system spins up in a single command.

## Why This Architecture Matters

The value of building this simulation is not the specific returns. It is the architecture patterns. Separation of signal generation from execution. Hard risk validation as a gating layer rather than an advisory one. Async coordination through a message bus that keeps agents decoupled. Observability built in through a dedicated reporting agent.

These patterns apply to much more than trading. Any domain where you need multiple specialized agents working on a shared problem, making decisions that affect each other, can benefit from this architecture. The message bus, the separation of roles, the risk validation gate. These are general solutions.

NEO built this as a simulation because trading makes the coordination challenges obvious. Real money on the line means poor coordination has immediate, measurable consequences.

## Watch It in Action

NEO recorded the full swarm running through a live simulation, with the message bus logs and per-agent trade activity visible in real time.

[![Watch on YouTube](https://img.youtube.com/vi/2c9pnt5i7jU/maxresdefault.jpg)](https://youtu.be/2c9pnt5i7jU)

---

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python multi-agent trading simulation with 10 specialized agents: 3 analyst agents that generate buy/sell signals from technical indicators, 4 trader agents that submit orders based on those signals, 2 risk manager agents that validate every order against position limits and stop-loss rules before execution, and 1 reporter agent that aggregates metrics. Coordinate all agents through an async publish/subscribe message bus — agents never call each other directly. Use Pydantic for message schema validation, yfinance for historical S&P 500 data, and Docker Compose for deployment. Simulate $1M capital across 250 trading days."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20Python%20multi-agent%20trading%20simulation%20with%2010%20specialized%20agents%3A%203%20analyst%20agents%20that%20generate%20buy%2Fsell%20signals%20from%20technical%20indicators%2C%204%20trader%20agents%20that%20submit%20orders%20based%20on%20those%20signals%2C%202%20risk%20manager%20agents%20that%20validate%20every%20order%20against%20position%20limits%20and%20stop-loss%20rules%20before%20execution%2C%20and%201%20reporter%20agent%20that%20aggregates%20metrics.%20Coordinate%20all%20agents%20through%20an%20async%20publish%2Fsubscribe%20message%20bus%20%E2%80%94%20agents%20never%20call%20each%20other%20directly.%20Use%20Pydantic%20for%20message%20schema%20validation%2C%20yfinance%20for%20historical%20S%26P%20500%20data%2C%20and%20Docker%20Compose%20for%20deployment.%20Simulate%20%241M%20capital%20across%20250%20trading%20days." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the message bus, all 10 agent classes, Pydantic message schemas, and Docker Compose configuration. From there you iterate — ask it to add configurable stop-loss thresholds per trader agent, add a `--start-date` flag to run the simulation over different market periods, or add real-time per-agent logging with structured JSON output for post-run analysis.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/Stock-trading-Agent-Swarm
cd Stock-trading-Agent-Swarm
pip install -r requirements.txt
python run_simulation.py
```

The Reporter agent streams per-agent activity to stdout as the simulation runs and writes a full summary to `./output/simulation_report.json` when complete — showing total return, trade count, approval rate, and positions blocked by risk managers.

NEO built a 10-agent trading simulation where asynchronous message-bus coordination, hard risk validation gates, and separation of signal generation from execution demonstrate the coordination patterns that make multi-agent systems reliable under real conditions. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
