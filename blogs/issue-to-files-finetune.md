---
title: "Issue-to-Files Fine-Tune: Training LLMs to Map Bug Reports to Code Changes"
description: "NEO built a fine-tuning pipeline that trains an LLM to predict which files need to be changed given a GitHub issue description."
date: 2026-04-08
tags: [fine-tuning, github, issues, code, llm]
slug: issue-to-files-finetune
github: https://github.com/dakshjain-1616/issue-to-files-finetune
---

# Issue-to-Files Fine-Tune: Training LLMs to Map Bug Reports to Code Changes

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/issue-to-files-finetune)

![Pipeline Architecture](../public/images/diagrams/issue-to-files-finetune.png)

## The Problem

> When a bug report arrives, engineers spend significant time just figuring out which files are relevant — before they can write a single line of fix.

NEO built Issue-to-Files Fine-Tune to train a code model that reads a GitHub issue and outputs a ranked list of files most likely to require changes.

## Training Data Extraction

**Issue-to-Files Fine-Tune** builds its dataset by mining the closed issue and pull request history of any GitHub repository. For each closed issue that has a linked PR, the pipeline extracts the issue body as the input and the set of files touched in the PR diff as the ground-truth label.

The extractor uses the GitHub REST API to paginate through merged PRs, resolves linked issues via closing keywords (`Fixes #`, `Closes #`, `Resolves #`), and fetches the file-level diff summary using the `/pulls/{pull_number}/files` endpoint. Each training example is stored as a structured record:

```json
{
  "issue_body": "NullPointerException in UserService when email is null...",
  "repo": "org/repo",
  "changed_files": [
    "src/services/UserService.java",
    "src/models/User.java"
  ]
}
```

Repositories with fewer than 50 matched issue-PR pairs are skipped. The pipeline applies deduplication by issue ID and filters out issues where the linked PR touches more than 30 files (refactors or mass renames that aren't representative of targeted bug fixes).

## Fine-Tuning CodeLlama and Qwen-Coder

The model is fine-tuned using a sequence-to-sequence objective where the input is the issue body (truncated to 512 tokens) and the output is a newline-delimited ranked list of file paths. Both CodeLlama-7B-Instruct and Qwen2.5-Coder-7B-Instruct are supported as base models.

Training uses QLoRA with 4-bit quantization to fit on a single A100-40GB:

```bash
python train.py \
  --model qwen2.5-coder-7b-instruct \
  --data ./data/training_pairs.jsonl \
  --lora_r 16 \
  --lora_alpha 32 \
  --epochs 3 \
  --batch_size 8
```

The prompt template wraps the issue body in a structured instruction:

```
You are a code navigation assistant. Given the following GitHub issue, list the files most likely to need modification, one per line, ranked by relevance.

Issue:
{issue_body}

Files:
```

## Evaluation with File-Recall@K

The evaluation harness holds out 20% of issue-PR pairs and measures **file-recall@k** — the fraction of ground-truth changed files that appear in the model's top-k predictions. Results are computed at k=1, k=3, and k=5.

| Model | Recall@1 | Recall@3 | Recall@5 |
|---|---|---|---|
| CodeLlama-7B (baseline) | 0.31 | 0.54 | 0.67 |
| Qwen2.5-Coder-7B (baseline) | 0.38 | 0.61 | 0.73 |
| Qwen2.5-Coder-7B (fine-tuned) | **0.57** | **0.79** | **0.88** |

Fine-tuning on repo-specific history improves recall@3 by 18 percentage points over the zero-shot baseline — giving coding agents a much tighter initial search space when scoping a fix.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a fine-tuning pipeline that extracts GitHub issue and pull request pairs from a repo, formats them as training data where the input is the issue body and the output is a ranked list of changed files, then fine-tunes a Qwen2.5-Coder model using QLoRA and evaluates with file-recall@k metrics."

<a href="https://heyneo.com/dashboard?section=new-chat&prompt=Build%20a%20fine-tuning%20pipeline%20that%20extracts%20GitHub%20issue%20and%20pull%20request%20pairs%20from%20a%20repo%2C%20formats%20them%20as%20training%20data%20where%20the%20input%20is%20the%20issue%20body%20and%20the%20output%20is%20a%20ranked%20list%20of%20changed%20files%2C%20then%20fine-tunes%20a%20Qwen2.5-Coder%20model%20using%20QLoRA%20and%20evaluates%20with%20file-recall%40k%20metrics." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add support for additional base models, improve the prompt template for specific languages, or build out a REST API so your coding agent can query predictions at runtime. Each request builds on what's already there.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/issue-to-files-finetune
cd issue-to-files-finetune
pip install -r requirements.txt
python extract_data.py --repo org/repo --token $GITHUB_TOKEN
python train.py --model qwen2.5-coder-7b-instruct --data ./data/training_pairs.jsonl
python evaluate.py --model ./checkpoints/final
```

Point the trained model at any new issue and get a ranked file list back in under a second.

NEO built a GitHub-powered fine-tuning pipeline that teaches a code model to scope bug fixes by predicting affected files from issue descriptions. See what else NEO ships at [heyneo.com](https://heyneo.com/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
