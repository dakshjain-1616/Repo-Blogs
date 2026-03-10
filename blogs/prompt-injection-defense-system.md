---
title: "How We Built a Prompt Injection Defense System with 98.9% Detection Accuracy"
description: "NEO built a production-ready, multi-layer prompt injection defense system that detects adversarial LLM attacks with 98.9% accuracy and under 200ms latency. Here's how it works."
date: 2026-03-09
tags: [prompt injection, LLM security, AI safety, adversarial attacks, toxic-bert, constitutional AI]
slug: prompt-injection-defense-system
github: https://github.com/dakshjain-1616/Prompt-Injection-Defence-System
---

# How We Built a Prompt Injection Defense System with 98.9% Detection Accuracy

[View the code on GitHub](https://github.com/dakshjain-1616/Prompt-Injection-Defence-System)

Security for large language models remains an unsolved problem in most production systems. The standard approach is to bolt on a basic content filter and call it done. We took a different approach: a proper, layered defense system that treats prompt injection as a first-class threat, tested against over 1,000 adversarial scenarios.

The result: 98.9% overall detection accuracy, a 0.4% false positive rate, and sub-200ms latency. Here is what we built and why it matters.

## The Problem with LLM Security Today

Prompt injection attacks are not theoretical. Attackers craft inputs designed to override a model's system instructions, switch its operating persona, or extract sensitive information it was trained to protect. Instruction override attacks, role-switching attacks, jailbreaks that use fictional framing or encoded text. The attack surface is wide.

A single content filter does not cut it. Pattern matching alone fails against novel attack variants. You need depth.

## Three Layers of Defense

We designed the system around three independent defensive layers, each catching a different class of attack.

### Layer 1: Input Sanitization

The first layer runs pattern recognition across the raw input before it ever reaches the model. We built a rule set targeting known injection signatures: phrases that attempt to override instructions, attempts to access system prompts, and common jailbreak templates. This layer is fast. It adds almost no latency because it runs before any model inference.

Known attack patterns are caught here. Novel patterns pass through to the next layer.

### Layer 2: Constitutional AI Evaluation

The second layer evaluates inputs against a set of ethical principles, inspired by the Constitutional AI framework. Rather than looking for specific attack strings, this layer asks a higher-level question: does this input attempt to make the model violate its operating principles?

This catches adversarial inputs that are syntactically novel but semantically dangerous. Role-switching prompts that use indirect language. Attacks embedded in creative writing framing. Social engineering attempts.

### Layer 3: ML-Powered Output Validation

The third layer evaluates model outputs using `toxic-bert`, a fine-tuned BERT model for toxicity classification. Even if a malicious input slips through the first two layers, this layer checks whether the output itself contains harmful content before it reaches the user. We scored 98% accuracy on toxicity classification using this model alone.

This is the backstop. Outputs are scored, and anything above the toxicity threshold is blocked and logged.

## Performance in Production

We tested the full pipeline across 1,000+ adversarial scenarios, covering every major attack category in current research.

- Instruction override attacks: 100% detection rate
- Role-switching attacks: 100% detection rate
- Overall detection accuracy: 98.9%
- False positive rate: 0.4%
- End-to-end latency: under 200ms with GPU acceleration

That false positive rate matters as much as the detection rate. A defense system that blocks 30% of legitimate traffic is not deployable. At 0.4%, this system is production-viable.

## Deployment

We ship this with Docker configuration built for security hardening. The container runs as a non-root user, mounts the filesystem read-only, and enforces resource limits. Kubernetes deployment specs are included for teams running at enterprise scale.

Setup requires Python 3.12+ and a free HuggingFace account to pull the toxicity model. The automated setup scripts handle environment configuration on both macOS/Linux and Windows.

## Where This Gets Used

The obvious use case is protecting any customer-facing LLM application. Chatbots, copilots, document Q&A systems. Anywhere user input touches a language model is a potential attack surface.

Beyond that, this is critical infrastructure for agentic systems. When an LLM agent can take real actions in the world, prompt injection is not just an annoyance. It is a direct security vulnerability. A well-crafted injection could redirect an agent's actions entirely.

Medical platforms, legal document tools, financial advisory systems. Any domain where a compromised model output carries real-world consequences needs a defense like this.

## What is Next

The current system is extensible. We are working on adding semantic similarity analysis to catch paraphrased attacks that share meaning but not surface form, and custom detection rules for domain-specific attack patterns.

Integrations with REST APIs and monitoring dashboards are on the roadmap so security teams can observe attack patterns over time, not just block them in the moment.

---

If you are building an LLM application and need a defense system that holds up under adversarial testing, NEO builds this infrastructure. We design with real threat models, not best-guess safety filters.

Check out what else we are working on at [heyneo.so](https://heyneo.so).
