---
title: "FinTradeBench CLI: Rigorous Backtesting for AI Trading Strategies"
description: "NEO built FinTradeBench CLI, a command-line tool for benchmarking AI-generated trading signals against historical financial data across stocks, crypto, forex, and commodities."
date: 2026-03-23
tags: [algorithmic trading, backtesting, financial AI, CLI, Sharpe ratio, quantitative finance]
slug: fintrade-bench-cli
github: https://github.com/dakshjain-1616/FinTradeBench-CLI
---

# FinTradeBench CLI: Rigorous Backtesting for AI Trading Strategies

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/FinTradeBench-CLI)

![Pipeline Architecture](../public/images/diagrams/fintrade-bench-cli.png)

## The Problem

> AI-generated trading signals are easy to produce and hard to evaluate honestly. A model that describes its strategy in compelling terms may be curve-fitting on recent data, generating signals indistinguishable from a random walk, or outperforming on raw return while hiding catastrophic drawdown risk. Without rigorous backtesting infrastructure, teams either skip evaluation or build bespoke scripts that are slow, inconsistent, and hard to share.

NEO built FinTradeBench CLI to provide a disciplined, reproducible backtesting pipeline for AI trading strategies — covering four asset classes, computing the full suite of professional risk metrics, and making it easy to compare AI-generated signals against classical technical indicators on the same historical dataset.

## Loading and Normalizing Historical Data

FinTradeBench CLI ingests historical OHLCV (open, high, low, close, volume) data from multiple sources. For equities, it fetches from Yahoo Finance or accepts CSV files in a standard column format. For crypto, it integrates with Binance and Coinbase historical APIs. Forex and commodity data can be loaded via OANDA or flat files.

All data passes through a normalization pipeline before any analysis runs. The pipeline checks for gaps in the time series, handles corporate actions for equities (dividend adjustments, stock splits), aligns timestamps across assets in a portfolio, and converts everything to a unified bar format. Data quality issues — missing bars, stale prices, zero-volume bars — are logged and either filled or flagged depending on the configured handling policy. Getting this right matters: a single corrupt bar can corrupt an entire backtest with a spurious spike or drawdown.

The data pipeline also handles forward-looking bias. Price data is partitioned into a training window (used to calibrate any adaptive strategy parameters) and a test window (used for evaluation). The partition is enforced strictly — no data from the test window is visible during training.

## Running the Backtest

The core backtest engine simulates trading over the historical test period bar by bar. For each bar, it calls the registered signal generator — which may be an AI model, a rule-based system, or a combination — and receives a signal: long, short, flat, or a continuous position size. The engine then simulates trade execution at the next bar's open price, which is the standard conservative assumption for backtesting (assuming you cannot trade at the exact bar close where the signal was generated).

Transaction costs are modeled explicitly. You configure commission per trade, bid-ask spread, and slippage (the price impact of your trade size relative to bar volume). For strategies that trade frequently, transaction costs dominate performance and cannot be ignored. The engine tracks cash, position, and mark-to-market portfolio value at each bar, producing a full equity curve.

Portfolio-level backtesting is supported for multi-asset strategies. Position sizing follows either fixed fractional sizing (a fixed percentage of portfolio per trade) or volatility-targeting (scaling position size so each position contributes equal expected volatility to the portfolio). The volatility targeting mode uses a rolling window to estimate per-asset volatility and rebalances dynamically.

## Risk Metrics and Performance Analysis

The output of a FinTradeBench run is a comprehensive metrics report. The headline metrics are:

**Sharpe Ratio**: annualized excess return divided by annualized volatility of returns. This is the most widely used risk-adjusted return metric. The CLI computes it using daily returns, annualized to a standard 252 trading days.

**Maximum Drawdown**: the largest peak-to-trough decline in portfolio value over the test period. This is the single most important risk metric for strategies under real capital constraints — it tells you the worst loss you would have experienced if you had entered at the peak.

**Win Rate**: the fraction of closed trades that were profitable. Useful context for understanding strategy character — a high-frequency strategy with a 55% win rate and small average gain looks very different from a trend-following strategy with a 35% win rate and large average gain.

**Alpha vs. Benchmark**: excess return over a passive buy-and-hold benchmark (typically the index or a representative ETF for the asset class). A strategy with positive alpha generates return beyond what you would have gotten by simply holding the market.

The report also includes annualized return, annualized volatility, Calmar ratio (annualized return divided by maximum drawdown), Sortino ratio (downside deviation version of Sharpe), average trade duration, and a breakdown of performance by month and by year.

## Comparing AI Signals to Classical Indicators

A key feature of FinTradeBench CLI is the comparison mode. Instead of just evaluating a single strategy, you can define a benchmark strategy using classical technical indicators and run both strategies on the same historical data in a single command.

Built-in technical indicator signals include moving average crossover (configurable fast and slow periods), RSI mean-reversion (buy oversold, sell overbought), Bollinger Band breakout, MACD, and momentum. These are the standard baselines that quantitative researchers use to calibrate whether a new signal is genuinely adding information.

The comparison report renders side by side: AI strategy vs. indicator baseline, across every metric. It includes a correlation analysis of the two signal series to quantify how independent the strategies are. If your AI model's signals are 95% correlated with a simple moving average crossover, it is probably learning to approximate the moving average — not discovering something novel. If they are largely uncorrelated but both profitable, that is genuinely interesting.

## CLI Interface and Reproducibility

Every FinTradeBench run is specified by a YAML config file and executed with a single command: `fintrade-bench run config.yaml`. The config specifies data source, asset, date range, strategy module path, benchmark indicator, cost model, and output format. Results are written to a directory with the equity curve as a CSV, the full metrics report as JSON, and a rendered HTML report with charts.

The combination of config-as-code and deterministic execution means every result is reproducible. Share the config file and the data source specification, and anyone can reproduce the exact same backtest numbers. This matters for reporting results honestly and for debugging when metrics change unexpectedly after a strategy update.

## How to Build This

Clone and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/FinTradeBench-CLI
cd FinTradeBench-CLI
pip install -r requirements.txt
```

Add your OpenRouter API key to a `.env` file:

```bash
cp .env.example .env
# Edit .env and set OPENROUTER_API_KEY
```

Run a full benchmark against a specific model:

```bash
python benchmark.py --model openai/gpt-4o
```

To try the tool without spending API credits:

```bash
python benchmark.py --model openai/gpt-4o --dry-run
```

To benchmark two models side by side:

```bash
python benchmark.py --compare openai/gpt-4o deepseek/deepseek-chat
```

The terminal shows a live progress bar as each of the 65 financial questions is answered, followed by a category breakdown table and per-question results. After the run, a JSON report and an HTML report with animated bar charts are saved automatically. A persistent leaderboard accumulates results across runs, so you can compare model performance over time with `python benchmark.py --leaderboard`.

NEO built FinTradeBench CLI so that evaluating AI trading strategies is as disciplined as evaluating any other machine learning system — data partitioning, cost modeling, risk metrics, and baseline comparison all enforced by the tool. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
