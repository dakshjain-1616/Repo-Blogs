---
title: "Orbit: Explore Your Codebase's Dependency Graph in 3D"
description: "NEO built Orbit, a 3D interactive visualization tool that renders Python, JavaScript, and TypeScript import graphs as force-directed networks to identify circular dependencies, orphaned modules, and architectural bottlenecks."
date: 2026-03-23
tags: [developer tools, dependency analysis, 3D visualization, Three.js, code architecture, static analysis]
slug: orbit-dependency-3d-visualiser
github: https://github.com/dakshjain-1616/Orbit-dependency-visualised
---

# Orbit: Explore Your Codebase's Dependency Graph in 3D

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/Orbit-dependency-visualised)

![Pipeline Architecture](../public/images/diagrams/orbit-dependency-3d-visualiser.png)

## The Problem

> Dependency graphs in large codebases are too complex to reason about as flat text. A module list tells you what exists. A flat 2D graph tells you what connects to what. Neither tells you the shape of the system: which modules are central load-bearing nodes, which are isolated islands, and which clusters have formed that should have stayed separate. At scale, these architectural problems are invisible until they cause outages or make refactoring nearly impossible.

NEO built Orbit to make dependency structure visible and explorable — not as a static diagram, but as an interactive 3D environment.

## The Analysis Layer: Parsing Import Graphs

Orbit starts with static analysis of the codebase. For Python, it uses the `ast` module to parse every `.py` file and extract import statements — both `import x` and `from x import y` forms. It resolves relative imports using the package structure, so `from ..utils import helpers` is correctly attributed to the right module rather than treated as an unresolved reference.

For JavaScript and TypeScript, Orbit uses the TypeScript compiler API to parse `import` and `require` statements, resolving path aliases from `tsconfig.json` and `jsconfig.json`. This handles the common pattern of projects that alias `@/components` to `src/components` — Orbit resolves these correctly rather than showing them as external dependencies.

The output of the analysis layer is a directed graph: nodes are modules, edges are import relationships. Edge direction matters — A importing B means B is a dependency of A, not the reverse. Both forms are tracked and stored so visualization can show either direction.

The graph is serialized to JSON and cached with a hash of the source files. Subsequent runs that have not changed files skip re-analysis entirely, making Orbit fast enough to run on file-save in watch mode.

## The 3D Rendering Layer: Three.js Force-Directed Graph

The visualization is built on Three.js using a force-directed graph layout algorithm. Force-directed layout is the right choice for dependency graphs because it produces a visual arrangement that reflects the underlying structure: tightly coupled clusters pull together, loosely connected modules drift apart, and the overall shape of the system becomes apparent.

Each node is rendered as a sphere. Node size scales with in-degree — modules that many other modules import appear larger. This makes central shared utilities immediately visible. Node color encodes module type: application code, test files, configuration, and external dependencies each get a distinct color.

Edges are rendered as directional lines with arrowheads indicating dependency direction. Edge color encodes relationship type: regular imports appear in a neutral gray, circular dependencies are highlighted in red, and cross-layer dependencies (a UI component importing a database layer directly, for example) appear in orange when architectural rules are configured.

The camera can orbit (hence the name), zoom, and pan using mouse controls. Clicking a node highlights it and its immediate neighbors — all other nodes fade to reduce visual noise. This "focus mode" makes it possible to trace the dependency chain of a specific module without losing spatial context.

## Detecting Architectural Problems

Orbit's analysis layer runs several structural checks beyond basic graph construction.

**Circular dependency detection** uses Tarjan's strongly connected components algorithm. Any set of modules that form a cycle is flagged and highlighted in red in the visualization. The sidebar shows the cycle as an ordered list of modules so it can be resolved. Circular dependencies are a common source of import errors, difficult-to-test code, and subtle initialization order bugs.

**Orphaned module detection** identifies modules that are not imported by any other module in the project. These are candidates for deletion or may indicate dead code that accumulated over time.

**High fan-in analysis** identifies modules with unusually high in-degree (many modules depend on them). These are architectural chokepoints — changing them requires coordinating updates across many parts of the codebase. Orbit highlights these and provides a list of all dependents, making the blast radius of a change immediately quantifiable.

**Layer violation detection** is configurable via a `.orbit.json` config file. If the project has defined architectural layers (e.g., `ui`, `service`, `repository`, `model`), Orbit can enforce that dependencies only flow in the permitted directions and highlight violations.

## Practical Use Cases

The most common use case for Orbit is architectural review before a major refactor. When a team needs to extract a module into a separate package, Orbit shows exactly which modules will need to change their imports — not as a surprise during the extraction, but as a planned list beforehand.

Onboarding is another high-value use case. A new developer can load Orbit on a codebase they have never seen and, within minutes, understand where the core business logic lives, which utilities are shared across the project, and which areas of the code are most interconnected. This understanding typically takes days to build from reading code alone.

During code review, Orbit in watch mode can show whether a PR is adding new circular dependencies or creating unexpected cross-layer couplings before the code merges.

## Performance at Scale

Orbit handles large codebases through progressive rendering. Projects with thousands of modules render a coarser-grained view initially — showing packages or directories as nodes rather than individual files — with the ability to expand a cluster into its constituent modules on demand. This keeps the visualization navigable even when the underlying graph has 10,000+ nodes.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a 3D dependency graph visualizer called Orbit for Python, JavaScript, and TypeScript codebases. Parse Python imports using the ast module (resolving relative imports), parse JS/TS imports using the TypeScript compiler API (resolving tsconfig.json path aliases). Render the directed graph with Three.js using a force-directed layout where node size scales with in-degree, node color encodes module type (app code, tests, config, external), and edge color distinguishes regular imports (gray), circular dependencies (red), and cross-layer violations (orange). Detect circular dependencies with Tarjan's algorithm, orphaned modules, and high fan-in nodes. Cache the graph JSON with a file hash so unchanged projects skip re-analysis."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%203D%20dependency%20graph%20visualizer%20called%20Orbit%20for%20Python%2C%20JavaScript%2C%20and%20TypeScript%20codebases.%20Parse%20Python%20imports%20using%20the%20ast%20module%20%28resolving%20relative%20imports%29%2C%20parse%20JS%2FTS%20imports%20using%20the%20TypeScript%20compiler%20API%20%28resolving%20tsconfig.json%20path%20aliases%29.%20Render%20the%20directed%20graph%20with%20Three.js%20using%20a%20force-directed%20layout%20where%20node%20size%20scales%20with%20in-degree%2C%20node%20color%20encodes%20module%20type%20%28app%20code%2C%20tests%2C%20config%2C%20external%29%2C%20and%20edge%20color%20distinguishes%20regular%20imports%20%28gray%29%2C%20circular%20dependencies%20%28red%29%2C%20and%20cross-layer%20violations%20%28orange%29.%20Detect%20circular%20dependencies%20with%20Tarjan%27s%20algorithm%2C%20orphaned%20modules%2C%20and%20high%20fan-in%20nodes.%20Cache%20the%20graph%20JSON%20with%20a%20file%20hash%20so%20unchanged%20projects%20skip%20re-analysis." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add layer violation detection driven by a `.orbit.json` config file, add `--watch` mode that rebuilds the graph on file save, or add progressive rendering that starts at package level and lets users expand clusters on demand for repos with thousands of modules.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/Orbit-dependency-visualised
cd Orbit-dependency-visualised
pip install -r requirements.txt
python orbit.py --path /path/to/your/project --language python
```

The visualization opens in your browser. Click any node to focus on it and its immediate neighbors; the sidebar lists detected circular dependencies and orphaned modules.

NEO built Orbit to make the invisible architecture of a codebase something you can see, explore, and reason about spatially. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
