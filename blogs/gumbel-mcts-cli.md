---
title: "Gumbel-MCTS-CLI: 10x Faster Tree Search in Pure Python"
description: "NEO built a pure-Python implementation of Gumbel-MCTS from the ICLR 2022 paper, benchmarked at ~10x faster than vanilla UCT with equivalent search quality, using NumPy only."
date: 2026-03-28
tags: [mcts, search, reinforcement-learning, numpy, algorithms]
slug: gumbel-mcts-cli
github: https://github.com/dakshjain-1616/gumbel-mcts-cli
---

# Gumbel-MCTS-CLI: 10x Faster Tree Search in Pure Python

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/gumbel-mcts-cli)

![Pipeline Architecture](../public/images/diagrams/gumbel-mcts-cli.png)

## The Problem

> Vanilla MCTS with UCB1 wastes simulation budget exploring actions that are clearly sub-optimal. As the tree grows, most simulations go to branches that will never be selected. The algorithm corrects itself eventually, but by then the time budget is gone.

NEO built Gumbel-MCTS-CLI to implement the fix from the ICLR 2022 paper by Danihelka, Guez, Schrittwieser, and Silver. The result runs approximately 10x faster than vanilla UCT at the same simulation budget, with equivalent or better search quality, using NumPy only with no GPU required.

## Three Changes from Vanilla MCTS

Gumbel-MCTS makes three targeted changes to the standard algorithm. Together they eliminate the wasted-simulation problem.

**Gumbel top-k sampling** replaces UCB exploration at the root. Instead of UCB scores, the algorithm adds Gumbel(0,1) noise to the log-prior probability of each action and selects the top-k candidates. This is statistically unbiased: under the right prior, the top-k actions are exactly the actions worth exploring. Budget goes to promising candidates from round one.

**Sequential halving** splits the simulation budget across log2(k) rounds. In each round, the bottom half of candidates is eliminated based on their current value estimates. By the final round, all remaining simulations go to the single most promising action. This is the technique from Successive Rejects adapted to tree search.

**Completed-Q values** fill in the value estimate for unvisited actions without running a rollout. The algorithm computes a weighted mean of visited siblings' Q-values, weighted by their priors. This makes early rounds cheap: you get a reasonable value estimate for every action before any simulation touches it.

The benchmark confirms the speedup is real. On the MaxTree environment with 200 simulations and 20 trials, vanilla MCTS takes 12.84ms per call. Gumbel-MCTS takes 1.31ms, a 9.80x speedup with a quality ratio of 1.13 (Gumbel finds slightly better solutions on average).

## The Three APIs

The tool exposes three search functions with different tradeoffs.

`search(env, state)` is the simple API. Call it, get the best action. No extra data returned.

`search_with_stats(env, state)` returns three values: best action, root node, and elapsed time in seconds. The root node has `value` (Q-value at root), `visit_count` (total simulations run), and a full child tree. Use this when you need to inspect the search tree after the fact.

`search_anytime(env, state)` is a generator that yields a snapshot after every sequential halving round. Each snapshot contains the current best action, round number, remaining candidates, elapsed time, and the full root node. Stop the generator at any point to get the best action found so far.

```python
# Budget-limited search: stop after 50ms
snapshot = None
for snapshot in agent.search_anytime(env, state):
    if snapshot['elapsed_sec'] > 0.050:
        break

best_action = snapshot['action']
```

The anytime API is important for real-time applications where you have a fixed time budget rather than a fixed simulation count.

## Tree Visualization

The tool ships an ASCII tree visualizer and an action statistics table. These are the primary debugging tools when the search is not finding the expected action.

```python
from gumbel_mcts.visualize import print_tree, format_action_table

best_action, root, elapsed = agent.search_with_stats(env, state)

print(print_tree(root, max_depth=3, max_children=5))
print(format_action_table(root, action_names={0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}))
```

The tree view shows visit count and Q-value for each node with a bar chart indicator. The action table shows visits, share percentage, Q-value, standard error, and prior for each root action. If the model's prior assigns 0.25 to each action (uniform) but visits are concentrated on action 1, that is Gumbel noise working correctly. If visits are still uniform after 200 simulations, the prior or the value function is flat and the search has no signal to exploit.

## Three Benchmark Environments

All three environments implement the same four-method protocol: `actions()`, `step(action)`, `clone()`, and `random_rollout()`. Any class implementing these four methods works as a drop-in environment for both `GumbelMCTS` and `VanillaMCTS`.

**GridWorld** is an 8x8 grid navigation task. The agent starts at (0,0) and must reach (N-1, N-1). Actions are UP, DOWN, LEFT, RIGHT. This tests search in a space with a clear optimal path.

**MaxTree** is a tree with depth 6 and branching factor 8. The agent selects actions to reach a leaf with the highest value. Since most leaves have low value, this tests the algorithm's ability to find the rare high-value path efficiently.

**SequenceEnv** builds a token sequence of length 5 from a vocabulary of 8 tokens. The score is a function of the sequence. This tests search in a combinatorial space without spatial structure.

## Custom Environments

Any environment that implements the four required methods plugs in directly.

```python
class MyEnv:
    def actions(self):           # list of valid actions
        ...
    def step(self, action):      # (next_state, reward, terminal)
        ...
    def clone(self):             # deep copy for tree simulation
        ...
    def random_rollout(self, env, depth):  # float value estimate
        ...

from gumbel_mcts.gumbel_mcts import GumbelMCTS

agent = GumbelMCTS(n_simulations=400, max_considered_actions=8)
best = agent.search(MyEnv(), initial_state)
```

The `clone()` method is required because MCTS simulates forward from each node, modifying state, then needs to restore the original state for the next simulation. The implementation must return a fully independent copy.

## How to Build This

Clone and install (NumPy only, no GPU):

```bash
git clone https://github.com/dakshjain-1616/gumbel-mcts-cli
cd gumbel-mcts-cli
pip install -r requirements.txt
```

Run the quick start example:

```python
from gumbel_mcts.gumbel_mcts import GumbelMCTS
from gumbel_mcts.env import GridWorldEnv

env = GridWorldEnv(size=8)
state = env.reset()

agent = GumbelMCTS(n_simulations=200, max_considered_actions=16)
best_action, root, elapsed = agent.search_with_stats(env, state)

print(f"Best action: {best_action}  ({elapsed*1000:.1f} ms)")
```

Run the CLI benchmark:

```bash
# Default: MaxTree, 20 trials, 200 simulations
python benchmark_mcts.py

# GridWorld, 50 trials
python benchmark_mcts.py --env gridworld --trials 50

# Quick dry-run (5 trials, 40 sims)
python benchmark_mcts.py --dry-run
```

The benchmark prints the full speedup table comparing Gumbel-MCTS and vanilla UCT side by side. Run the test suite:

```bash
pytest tests/ -q
# 88 passed
```

NEO built a pure-Python Gumbel-MCTS implementation from the ICLR 2022 paper that runs 10x faster than vanilla UCT with no GPU required and a simple four-method protocol for custom environments. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
