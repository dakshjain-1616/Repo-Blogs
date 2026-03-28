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

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Implement Gumbel-MCTS from the ICLR 2022 paper by Danihelka, Guez, Schrittwieser, and Silver in pure Python using NumPy only. The three key changes from vanilla UCT are: Gumbel top-k sampling at the root (add Gumbel(0,1) noise to log-prior probabilities and select top-k candidates), sequential halving (split simulation budget across log2(k) rounds, eliminating bottom half each round), and completed-Q values (fill unvisited action value estimates using prior-weighted sibling Q-values). Expose three APIs: search() returning the best action, search_with_stats() returning action/root node/elapsed time, and search_anytime() as a generator yielding snapshots after each sequential halving round for budget-limited stopping. Include three benchmark environments: 8x8 GridWorld, MaxTree (depth 6, branching factor 8), and SequenceEnv (5-token sequence, vocabulary 8). Any class implementing actions()/step()/clone()/random_rollout() works as a drop-in environment."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Implement%20Gumbel-MCTS%20from%20the%20ICLR%202022%20paper%20by%20Danihelka%2C%20Guez%2C%20Schrittwieser%2C%20and%20Silver%20in%20pure%20Python%20using%20NumPy%20only.%20The%20three%20key%20changes%20from%20vanilla%20UCT%20are%3A%20Gumbel%20top-k%20sampling%20at%20the%20root%20%28add%20Gumbel%280%2C1%29%20noise%20to%20log-prior%20probabilities%20and%20select%20top-k%20candidates%29%2C%20sequential%20halving%20%28split%20simulation%20budget%20across%20log2%28k%29%20rounds%2C%20eliminating%20bottom%20half%20each%20round%29%2C%20and%20completed-Q%20values%20%28fill%20unvisited%20action%20value%20estimates%20using%20prior-weighted%20sibling%20Q-values%29.%20Expose%20three%20APIs%3A%20search%28%29%20returning%20the%20best%20action%2C%20search_with_stats%28%29%20returning%20action%2Froot%20node%2Felapsed%20time%2C%20and%20search_anytime%28%29%20as%20a%20generator%20yielding%20snapshots%20after%20each%20sequential%20halving%20round%20for%20budget-limited%20stopping.%20Include%20three%20benchmark%20environments%3A%208x8%20GridWorld%2C%20MaxTree%20%28depth%206%2C%20branching%20factor%208%29%2C%20and%20SequenceEnv%20%285-token%20sequence%2C%20vocabulary%208%29.%20Any%20class%20implementing%20actions%28%29%2Fstep%28%29%2Fclone%28%29%2Frandom_rollout%28%29%20works%20as%20a%20drop-in%20environment." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation from that. From there you iterate — ask it to add the ASCII tree visualizer and action statistics table showing visit counts, Q-values, and priors for debugging search behavior, add the CLI benchmark script that runs both Gumbel-MCTS and vanilla UCT side by side and prints a speedup table, or add the 88-test pytest suite covering all three APIs and environments. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/gumbel-mcts-cli
cd gumbel-mcts-cli
pip install -r requirements.txt
python benchmark_mcts.py --dry-run
```

The benchmark prints the full speedup table comparing Gumbel-MCTS and vanilla UCT side by side — the default MaxTree run shows approximately 10x faster search at equivalent or better solution quality.

NEO built a pure-Python Gumbel-MCTS implementation from the ICLR 2022 paper that runs 10x faster than vanilla UCT with no GPU required and a simple four-method protocol for custom environments. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
