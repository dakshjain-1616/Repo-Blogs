---
title: "How NEO Built a Prompt Injection Defense System with 98.9% Detection Accuracy"
description: "NEO built a production-ready, multi-layer prompt injection defense system that detects adversarial LLM attacks with 98.9% accuracy and under 200ms latency. Here's how it works."
date: 2026-03-09
tags: [prompt injection, LLM security, AI safety, adversarial attacks, toxic-bert, constitutional AI]
slug: prompt-injection-defense-system
github: https://github.com/dakshjain-1616/Prompt-Injection-Defence-System
---

# How NEO Built a Prompt Injection Defense System with 98.9% Detection Accuracy

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/Prompt-Injection-Defence-System)

![Pipeline Architecture](../public/images/diagrams/prompt-injection-defense-system.png)

## The Problem

> Prompt injection attacks are not theoretical. Attackers craft inputs designed to override a model's system instructions, switch its operating persona, or extract sensitive information it was trained to protect. The standard approach — bolt on a basic content filter and call it done — fails against novel attack variants, because pattern matching alone can't keep up with the attack surface. For agentic systems that take real-world actions, a successful injection isn't just an annoyance: it's a direct security vulnerability.

NEO took a different approach: a proper, layered defense system that treats prompt injection as a first-class threat, tested against over **1,000 adversarial scenarios**. The result: **98.9% overall detection accuracy**, a **0.4% false positive rate**, and **sub-200ms latency**.

## Three Layers of Defense

NEO designed the system around three independent defensive layers, each catching a different class of attack.

### Layer 1: Input Sanitization

The first layer runs pattern recognition across the raw input before it ever reaches the model. NEO built a rule set targeting known injection signatures: phrases that attempt to override instructions, attempts to access system prompts, and common jailbreak templates. This layer is fast. It adds almost no latency because it runs before any model inference.

Known attack patterns are caught here. Novel patterns pass through to the next layer.

### Layer 2: Constitutional AI Evaluation

The second layer evaluates inputs against a set of ethical principles, inspired by the Constitutional AI framework. Rather than looking for specific attack strings, this layer asks a higher-level question: does this input attempt to make the model violate its operating principles?

This catches adversarial inputs that are syntactically novel but semantically dangerous. Role-switching prompts that use indirect language. Attacks embedded in creative writing framing. Social engineering attempts.

### Layer 3: ML-Powered Output Validation

The third layer evaluates model outputs using `toxic-bert`, a fine-tuned BERT model for toxicity classification. Even if a malicious input slips through the first two layers, this layer checks whether the output itself contains harmful content before it reaches the user. NEO scored 98% accuracy on toxicity classification using this model alone.

This is the backstop. Outputs are scored, and anything above the toxicity threshold is blocked and logged.

## Performance in Production

NEO tested the full pipeline across 1,000+ adversarial scenarios, covering every major attack category in current research.

- **Instruction override attacks: 100% detection rate**
- **Role-switching attacks: 100% detection rate**
- **Overall detection accuracy: 98.9%**
- **False positive rate: 0.4%**
- End-to-end latency: under **200ms** with GPU acceleration

That false positive rate matters as much as the detection rate. A defense system that blocks 30% of legitimate traffic is not deployable. At 0.4%, this system is production-viable.

## Deployment

NEO ships this with Docker configuration built for security hardening. The container runs as a non-root user, mounts the filesystem read-only, and enforces resource limits. Kubernetes deployment specs are included for teams running at enterprise scale.

Setup requires Python 3.12+ and a free HuggingFace account to pull the toxicity model. The automated setup scripts handle environment configuration on both macOS/Linux and Windows.

## Where This Gets Used

The obvious use case is protecting any customer-facing LLM application. Chatbots, copilots, document Q&A systems. Anywhere user input touches a language model is a potential attack surface.

Beyond that, this is critical infrastructure for agentic systems. When an LLM agent can take real actions in the world, prompt injection is not just an annoyance. It is a direct security vulnerability. A well-crafted injection could redirect an agent's actions entirely.

Medical platforms, legal document tools, financial advisory systems. Any domain where a compromised model output carries real-world consequences needs a defense like this.

## What is Next

The current system is extensible. NEO is working on adding semantic similarity analysis to catch paraphrased attacks that share meaning but not surface form, and custom detection rules for domain-specific attack patterns.

Integrations with REST APIs and monitoring dashboards are on the roadmap so security teams can observe attack patterns over time, not just block them in the moment.

---

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a three-layer prompt injection defense system in Python 3.12 that runs as a Flask REST API. Layer 1: rule-based input sanitization with regex patterns targeting instruction-override phrases, system prompt access attempts, and jailbreak templates. Layer 2: Constitutional AI evaluation that checks whether the input attempts to make the model violate its operating principles, catching novel phrasing and role-switching attacks. Layer 3: toxic-bert output validation that classifies model outputs before they reach the user and blocks anything above a toxicity threshold. Return a JSON response with detection verdict, which layer caught it, confidence score, and whether it was blocked. Log blocked inputs with timestamp and attack category."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20three-layer%20prompt%20injection%20defense%20system%20in%20Python%203.12%20that%20runs%20as%20a%20Flask%20REST%20API.%20Layer%201%3A%20rule-based%20input%20sanitization%20with%20regex%20patterns%20targeting%20instruction-override%20phrases%2C%20system%20prompt%20access%20attempts%2C%20and%20jailbreak%20templates.%20Layer%202%3A%20Constitutional%20AI%20evaluation%20that%20checks%20whether%20the%20input%20attempts%20to%20make%20the%20model%20violate%20its%20operating%20principles%2C%20catching%20novel%20phrasing%20and%20role-switching%20attacks.%20Layer%203%3A%20toxic-bert%20output%20validation%20that%20classifies%20model%20outputs%20before%20they%20reach%20the%20user%20and%20blocks%20anything%20above%20a%20toxicity%20threshold.%20Return%20a%20JSON%20response%20with%20detection%20verdict%2C%20which%20layer%20caught%20it%2C%20confidence%20score%2C%20and%20whether%20it%20was%20blocked.%20Log%20blocked%20inputs%20with%20timestamp%20and%20attack%20category." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation. From there you iterate — ask it to add a security-hardened Docker configuration that runs as non-root with a read-only filesystem and all capabilities dropped, add Kubernetes deployment specs for horizontal scaling, or add a `pytest` test suite that covers all 1,000+ adversarial scenarios across instruction override, role-switching, and social engineering attack categories.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/Prompt-Injection-Defence-System
cd Prompt-Injection-Defence-System
pip install -r requirements.txt
bash setup.sh
```

Once running, send any suspicious prompt to `POST /check` and get back a structured response showing which layer caught it and why.

NEO built a prompt injection defense system where three independent layers—input sanitization, constitutional AI evaluation, and ML-powered output validation—achieve 98.9% detection accuracy at a 0.4% false positive rate, making it deployable in production without blocking legitimate traffic. See what else NEO ships at [heyneo.so](https://heyneo.so()).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
