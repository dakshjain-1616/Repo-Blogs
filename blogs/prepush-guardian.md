---
title: "PrePush Guardian: AI-Powered Pre-Push Code Review and Safety Gate"
description: "NEO built a git pre-push hook that runs an LLM-powered code review on every diff before it reaches the remote, checking for security issues, breaking changes, missing test coverage, and style violations."
date: 2026-04-08
tags: [git, code-review, ci-cd, safety, llm]
slug: prepush-guardian
github: https://github.com/dakshjain-1616/prepush-guardian
---

# PrePush Guardian: AI-Powered Pre-Push Code Review and Safety Gate

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/prepush-guardian)

![Pipeline Architecture](../public/images/diagrams/prepush-guardian.png)

## The Problem

> Code review catches bugs, but it happens after the push. By then the diff is already on the remote, visible in CI, potentially merged by an auto-merge bot, or running in a preview environment. The earlier you catch a problem, the cheaper it is to fix.

NEO built PrePush Guardian to move a meaningful subset of code review — security, breaking changes, test coverage gaps, and style — to the moment before `git push` executes, when the developer is still local and fixing the issue takes seconds.

## Diff Analysis and Check Categories

**PrePush Guardian** installs as a standard git pre-push hook (`hooks/pre-push`). When triggered, it runs `git diff origin/<target-branch>...HEAD` to get the complete diff of all commits about to be pushed, then submits that diff to a configurable LLM endpoint for structured analysis.

The review is structured into four check categories, each with its own prompt and severity level:

**Security checks** look for hardcoded secrets (API keys, tokens, passwords matching common regex patterns), SQL injection vulnerabilities (string concatenation into query strings), and command injection risks (unsanitized input passed to `subprocess`, `exec`, or `os.system`). Security findings default to `BLOCK` severity — they prevent the push unless explicitly overridden.

**Breaking API changes** compare function and class signatures in the diff against any existing call sites found in the repo. If a public function's signature changes without a corresponding update to its callers, the check flags it. This requires a brief repo scan using `ast` parsing, which runs locally before the LLM call.

**Test coverage gaps** check whether changed files have corresponding changes in test files. The heuristic: if `src/payments.py` is modified but no file matching `test*payments*` or `tests/payments*` appears in the diff, the check flags missing coverage. The LLM adds a second pass, reading the changed functions and noting which ones have no obvious test analog.

**Style violations** enforce configurable rules: function length limits, docstring presence on public methods, and import ordering. These default to `WARN` severity — they appear in the output but do not block the push.

## GO/NO-GO Verdict and Line-Specific Comments

The LLM returns a structured JSON response with a verdict and an array of findings:

```json
{
  "verdict": "NO-GO",
  "findings": [
    {
      "file": "src/auth.py",
      "line": 42,
      "severity": "BLOCK",
      "category": "security",
      "detail": "Hardcoded API key assigned to `STRIPE_SECRET`. Move to environment variable."
    },
    {
      "file": "src/payments.py",
      "line": 118,
      "severity": "WARN",
      "category": "test-coverage",
      "detail": "Function `process_refund` added but no test file references it."
    }
  ]
}
```

PrePush Guardian renders this in the terminal with color-coded severity levels and file:line references that most terminals make clickable. The final line prints either `PUSH BLOCKED` in red or `PUSH APPROVED` in green, then exits with code 1 or 0 respectively to control whether git proceeds with the push.

## Severity Thresholds and Team Configuration

Every check category's blocking behavior is configurable in `.guardian.yml` at the repo root:

```yaml
thresholds:
  security: block       # BLOCK severity always stops push
  breaking-changes: block
  test-coverage: warn   # WARN severity logs but allows push
  style: warn

llm:
  provider: openai
  model: gpt-4o-mini   # fast and cheap for diff analysis
  max_tokens: 2048

ignore:
  paths:
    - "migrations/"
    - "*.generated.py"
```

Teams with stricter standards can promote `test-coverage` to `block`. Teams that want to disable style checking entirely can set `style: off`. The `ignore.paths` list lets teams skip generated files or migration scripts that would otherwise trigger false positives.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a git pre-push hook in Python called PrePush Guardian that extracts the full diff of commits about to be pushed, sends it to an LLM for structured code review across four categories: security issues (secrets, SQL injection, command injection), breaking API changes (signature changes without caller updates), missing test coverage (changed files without corresponding test changes), and style violations. Return a GO/NO-GO verdict with line-specific findings, configurable severity thresholds per category in a .guardian.yml file, and exit code 1 to block the push on BLOCK-severity findings."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20git%20pre-push%20hook%20in%20Python%20called%20PrePush%20Guardian%20that%20extracts%20the%20full%20diff%20of%20commits%20about%20to%20be%20pushed%2C%20sends%20it%20to%20an%20LLM%20for%20structured%20code%20review%20across%20four%20categories%3A%20security%20issues%20%28secrets%2C%20SQL%20injection%2C%20command%20injection%29%2C%20breaking%20API%20changes%20%28signature%20changes%20without%20caller%20updates%29%2C%20missing%20test%20coverage%20%28changed%20files%20without%20corresponding%20test%20changes%29%2C%20and%20style%20violations.%20Return%20a%20GO%2FNO-GO%20verdict%20with%20line-specific%20findings%2C%20configurable%20severity%20thresholds%20per%20category%20in%20a%20.guardian.yml%20file%2C%20and%20exit%20code%201%20to%20block%20the%20push%20on%20BLOCK-severity%20findings." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a `--dry-run` flag that shows what would be blocked without actually blocking, build a GitHub Actions workflow that runs the same checks on PRs, or extend the security checks with a custom regex pattern library for your team's secret formats. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/prepush-guardian
cd prepush-guardian
pip install -r requirements.txt
python install.py --repo /path/to/your/repo
```

The installer copies the hook script to your repo's `.git/hooks/pre-push` and writes a default `.guardian.yml`. Every subsequent `git push` in that repo will trigger the review automatically.

NEO built PrePush Guardian, a git pre-push hook that uses an LLM to review diffs for security issues, breaking changes, missing test coverage, and style violations before they reach the remote, with configurable severity thresholds that control what blocks vs. what only warns. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
