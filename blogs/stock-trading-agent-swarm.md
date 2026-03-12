---
title: "Stock Trading Agent Swarm: How NEO Coordinated 10 Specialized Agents on a Simulated Portfolio"
description: "NEO built a multi-agent trading simulation with 10 specialized agents coordinating over an async message bus, achieving +4.62% returns across 250 days of S&P 500 data with an 86.9% order approval rate."
date: 2026-03-09
tags: [multi-agent systems, trading simulation, agent swarm, async messaging, Python, financial AI]
slug: stock-trading-agent-swarm
github: https://github.com/dakshjain-1616/Stock-trading-Agent-Swarm
---

# Stock Trading Agent Swarm: How NEO Coordinated 10 Specialized Agents on a Simulated Portfolio

<a href="https://github.com/dakshjain-1616/Stock-trading-Agent-Swarm" target="_blank" style="display:flex;align-items:center;gap:14px;padding:16px 20px;border:1px solid #30363d;border-radius:10px;background:#0d1117;color:#e6edf3;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:20px 0;width:fit-content;max-width:480px;transition:border-color 0.2s;">
  <svg width="22" height="22" viewBox="0 0 16 16" fill="#e6edf3" xmlns="http://www.w3.org/2000/svg"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
  <div>
    <div style="font-weight:600;font-size:14px;color:#e6edf3;">dakshjain-1616/Stock-trading-Agent-Swarm</div>
    <div style="font-size:12px;color:#8b949e;margin-top:3px;">View on GitHub →</div>
  </div>
</a>

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

We recorded the full swarm running through a live simulation, with the message bus logs and per-agent trade activity visible in real time.

<a href="https://youtu.be/2c9pnt5i7jU" target="_blank" style="display:block;max-width:560px;margin:20px 0;border-radius:12px;overflow:hidden;border:1px solid #30363d;position:relative;cursor:pointer;text-decoration:none;">
  <img src="https://img.youtube.com/vi/2c9pnt5i7jU/maxresdefault.jpg" alt="Watch on YouTube" style="width:100%;display:block;">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.72);border-radius:50%;width:68px;height:68px;display:flex;align-items:center;justify-content:center;">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>
  </div>
  <div style="position:absolute;bottom:12px;left:16px;background:rgba(0,0,0,0.7);color:#fff;font-size:12px;padding:4px 10px;border-radius:4px;font-family:sans-serif;">▶ Watch on YouTube</div>
</a>

---

NEO built a 10-agent trading simulation where asynchronous message-bus coordination, hard risk validation gates, and separation of signal generation from execution demonstrate the coordination patterns that make multi-agent systems reliable under real conditions. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [**Install NEO for Cursor →**](cursor:extension/NeoResearchInc.heyneo)

---
