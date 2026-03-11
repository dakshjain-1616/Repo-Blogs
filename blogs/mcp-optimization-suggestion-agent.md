---
title: "Automating MCP Server Discovery: The NEO Optimization and Suggestion Agent"
description: "NEO built an intelligent agent that automates Model Context Protocol server discovery, configuration analysis, and optimization suggestions using live web research and AI reasoning."
date: 2026-03-09
tags: [mcp, model-context-protocol, ai-agent, claude-desktop, openrouter, automation, configuration]
slug: mcp-optimization-suggestion-agent
github: https://github.com/abhishekgandhi-neo/MCP_Optimization_Suggestion_Agent_By_NEO
---

# Automating MCP Server Discovery: The NEO Optimization and Suggestion Agent

[View the code on GitHub](https://github.com/abhishekgandhi-neo/MCP_Optimization_Suggestion_Agent_By_NEO)

![Pipeline Architecture](../public/images/diagrams/mcp-optimization-suggestion-agent.png)


If you've spent time configuring Model Context Protocol servers, you know the routine. Search GitHub. Filter through dozens of repos of varying quality. Read each README. Figure out if the tool actually fits your use case. Edit JSON by hand. Break something. Fix it. Repeat.

It's tedious, time-consuming work. So we automated it.

The MCP Optimization and Suggestion Agent does what you'd normally spend 30+ minutes doing: it researches available MCP servers across the web, reasons about which ones fit your needs, and either generates a tailored configuration from scratch or analyzes and improves your existing setup. The whole research cycle completes in 8 to 12 seconds.

## What the Agent Actually Does

There are two modes, each solving a different problem.

**Mode 1: Optimize what you have.** Point the agent at your existing MCP configuration file. It reads your current setup, identifies gaps and redundancies, then suggests improvements with specific configuration snippets. It creates a backup before touching anything, so you can always roll back.

**Mode 2: Start fresh from a use case.** Describe what you're trying to accomplish in plain text. The agent performs live web research, identifies relevant MCP servers, reasons about fit, and produces a full markdown report with recommended configurations, rationale, and implementation guidance.

Both modes produce structured, usable outputs. Not vague suggestions. Actual JSON configuration files and documentation you can act on immediately.

## The Technical Architecture

We built this on four distinct modules that chain together cleanly.

The **research module** handles web filtering. It queries live sources, not a static database, so it finds recently published servers that wouldn't appear in a hardcoded list. It applies filtering logic to suppress false positives, achieving roughly 90% precision in relevance filtering. When you ask for MCP servers that handle database access, you get database tools, not a random assortment.

The **AI agent module** takes the raw research and applies structured reasoning. It evaluates server quality, checks compatibility, and weighs tradeoffs between options. Raw search results are noise; the agent layer turns them into prioritized recommendations.

The **analysis engine** handles validation and optimization. It checks configuration syntax, identifies conflicts between servers, and verifies that suggested setups will actually work with Claude Desktop's expected format.

The **reporting module** produces the final outputs: markdown reports with full rationale, JSON configs ready to copy, and raw research data if you want to dig deeper.

The stack is Python 3.12+, Node.js 18+, and OpenRouter for model access. No proprietary infrastructure required.

## Why This Matters for MCP Users

MCP is still early. The ecosystem is growing fast, which means new servers appear constantly and the best options for any given workflow change over time. A static list of "recommended MCP servers" goes stale within weeks.

An agent that researches live is different. It finds things published last month. It catches deprecated packages. It notices when a popular server has been forked into something better.

This is especially useful for teams with multiple people configuring Claude Desktop. Instead of everyone independently googling and arriving at different setups, you run the agent once per use case and get a consistent, documented baseline configuration.

## What the Output Looks Like

For Mode 2, you get a markdown report organized by capability area. Each recommended server gets a section covering what it does, why it was selected over alternatives, the exact JSON configuration block, and any dependencies or setup steps needed.

For Mode 1, you get a diff-style view of your current configuration with specific improvement suggestions. The agent flags unused servers, recommends replacements for outdated tools, and suggests additions based on what your current setup implies about your workflow.

## Configuration and Integration

API setup requires a free key from openrouter.ai. After that, the CLI walks you through both modes. Generated configurations drop directly into Claude Desktop's expected directory structure.

```bash
# Analyze and optimize existing config
python agent.py --mode optimize --config ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Generate recommendations for a use case
python agent.py --mode suggest --task "I need MCP servers for web scraping, database queries, and file management"
```

The NEO VSCode extension integrates with the agent as well, letting you trigger configuration updates from within your editor without context switching.

## Practical Applications

This agent is useful any time you're setting up a new Claude Desktop environment, onboarding someone to an MCP-heavy workflow, auditing an existing configuration that has grown organically over time, or exploring capabilities you haven't yet set up.

It's also a concrete example of what an agentic research pipeline looks like in practice: live data retrieval, structured reasoning, validated output generation, and clean integration with existing tooling. No magic, just a well-designed pipeline.

If you want NEO to build a similar research-and-configuration agent for your own tooling or infrastructure, visit [heyneo.so](https://heyneo.so/) to get started.

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: [NEO in Cursor](cursor:extension/NeoResearchInc.heyneo)
