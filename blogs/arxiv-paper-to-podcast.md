---
title: "Arxiv Paper to Podcast: ML Research You Can Listen To"
description: "NEO built a pipeline that converts arxiv research papers into podcast-style audio episodes with two AI hosts, TTS voice synthesis, background music, and MP3 output — making ML research accessible through audio."
date: 2026-03-23
tags: [arxiv, podcast, TTS, LLM, research, audio, ML-accessibility, text-to-speech]
slug: arxiv-paper-to-podcast
github: https://github.com/dakshjain-1616/arxiv-paper-to-podcast
---

# Arxiv Paper to Podcast: ML Research You Can Listen To

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/arxiv-paper-to-podcast)

![Pipeline Architecture](../public/images/diagrams/arxiv-paper-to-podcast.png)

## The Problem

> Machine learning research moves faster than most people can read. Hundreds of papers land on arxiv every day, and the academic writing style — dense with notation, passive voice, and field-specific jargon — makes them slow to consume even for specialists. Researchers, engineers, and enthusiasts increasingly learn on the go: during commutes, workouts, or household tasks where reading is impossible. There is no good automated way to turn a research paper into something listenable.

NEO built an end-to-end pipeline that takes an arxiv paper ID or search query, fetches the paper, uses LLMs to transform the academic text into a natural two-host podcast conversation, synthesizes speech with distinct voices, adds background music, and produces a finished MP3 episode. The result makes ML research genuinely accessible through audio without requiring any manual writing or production work.

## Fetching and Parsing Papers

The pipeline's first stage handles paper retrieval from arxiv using the official arxiv API. Users can provide a paper ID directly (e.g., `2301.07041`) or a keyword search query, which returns the top-N most recent matching papers for batch episode generation.

Once retrieved, the paper content requires careful parsing. arxiv papers are available in PDF and LaTeX source formats. NEO chose to work with the PDF layer via a structured extraction pipeline rather than raw LaTeX, because LaTeX source has inconsistent structure and many authors use custom macros that complicate parsing. The PDF extraction uses layout-aware parsing that preserves section headers, identifies and discards figure captions and reference list entries, and flags mathematical notation blocks for special handling.

Mathematical notation is a specific challenge for audio conversion. Equations that appear inline in text — `the loss is L = -log p(y|x)` — need to be either read as natural language ("the loss equals negative log probability of y given x") or briefly described and moved on from. NEO built a notation-to-speech converter that handles common ML notation patterns: summation signs, partial derivatives, argmax expressions, and Greek letter variables. For complex multi-line equations, the converter generates a simplified verbal approximation and flags it as an approximation in the transcript.

## Academic Text to Conversational Dialogue

The transformation from academic text to podcast dialogue is the most technically demanding stage of the pipeline. Academic writing is optimized for precision and verifiability — it hedges every claim, defines every term, and structures arguments for review rather than comprehension. Podcast dialogue is optimized for engagement and retention — it uses concrete examples, rhetorical questions, and conversational asides to maintain listener attention.

NEO designed a two-pass LLM transformation process. The first pass extracts the paper's core contributions — typically the problem statement, the proposed method, the key results, and the main limitations — into a structured intermediate representation. This extraction step is deliberately separate from the dialogue generation step because mixing them in a single prompt produces output that rushes through important content and over-expands on minor details.

The second pass converts the structured intermediate representation into a two-host dialogue script. The two hosts have distinct roles: Host A is the generalist who asks questions a smart non-specialist might ask, while Host B is the domain expert who provides answers and context. This dynamic naturally produces the explanatory back-and-forth that makes technical content accessible without requiring the listener to have background knowledge.

The dialogue generation prompt includes specific instructions for handling uncertainty — when the paper's claims are qualified, the host dialogue should reflect that qualification rather than presenting results as stronger than the authors intended. This is an important accuracy safeguard for scientific communication.

## Voice Synthesis and Differentiation

The two-host format requires perceptibly distinct voices to remain listenable over a 15-20 minute episode. NEO implemented voice differentiation using a combination of TTS voice selection and post-processing.

The voice selection assigns distinct TTS voice profiles to each host, choosing voices that differ in pitch range, speaking rate, and timbre. Host A uses a mid-range voice with a slightly faster speaking rate that conveys curiosity and engagement. Host B uses a deeper voice with a slightly measured pace that conveys expertise.

Post-processing adds speaker-specific acoustic fingerprints using EQ and subtle reverb settings. Host B receives a slight low-frequency emphasis that adds authority, while Host A receives a slight high-frequency boost that adds brightness and energy. These are subtle effects — the goal is to aid listener orientation without calling attention to the processing.

Dialogue transitions include synthesized non-verbal markers — brief hesitations, affirmative sounds — that make the exchange sound more like a real conversation. NEO curated a small library of these markers and inserts them probabilistically at natural conversation boundaries.

## Background Music and Episode Assembly

Background music uses the same library and selection logic as the LumosX Personalizer pipeline: an embedding-based matcher that selects tracks appropriate to the content's mood and complexity. Science and ML content tends to match best with ambient electronic or light orchestral tracks that provide energy without distraction.

The music is mixed at -20dB relative to the speech, far enough under to be imperceptible during dialogue but audible during the intro, outro, and brief musical transitions between paper sections. Section transitions use a half-second music swell — a brief volume increase — to signal the listener that a new topic is beginning, analogous to a chapter marker.

The final assembly stage stitches the per-host audio segments, inserts transition music, adds the intro and outro, and renders to MP3 at 128kbps — standard for spoken word podcast audio. Each episode includes ID3 metadata: paper title, authors, arxiv ID, and generation date. The ID3 thumbnail uses the paper's first figure if available, or a generated cover image otherwise.

## Batch Generation and Integration

For researchers who want to convert an entire reading list, NEO built a batch mode that accepts a list of arxiv IDs from a text file and generates episodes sequentially, writing each to a configurable output directory. A companion RSS feed generator produces a valid podcast feed XML from the output directory, making it straightforward to subscribe to personal arxiv-to-podcast feeds in any podcast app.

A webhook mode supports integration with arxiv mailing list notifications — when new papers arrive in configured categories, the pipeline automatically generates episodes and appends them to the feed. This creates a true "subscribe and listen" workflow for staying current with ML research without reading queues that pile up faster than you can clear them.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python CLI tool that converts arxiv papers into podcast-style MP3 episodes. Fetch papers by ID or keyword search using the arxiv API, extract content with layout-aware PDF parsing that discards figure captions and reference lists, and convert inline math notation to speakable natural language. Use a two-pass LLM process: first extract the core problem, method, results, and limitations into a structured intermediate form, then generate a two-host dialogue script where Host A asks generalist questions and Host B answers as the domain expert. Synthesize each host's lines with distinct ElevenLabs voices, mix background music at -20dB, and assemble a finished MP3 with ID3 metadata."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20Python%20CLI%20tool%20that%20converts%20arxiv%20papers%20into%20podcast-style%20MP3%20episodes.%20Fetch%20papers%20by%20ID%20or%20keyword%20search%20using%20the%20arxiv%20API%2C%20extract%20content%20with%20layout-aware%20PDF%20parsing%20that%20discards%20figure%20captions%20and%20reference%20lists%2C%20and%20convert%20inline%20math%20notation%20to%20speakable%20natural%20language.%20Use%20a%20two-pass%20LLM%20process%3A%20first%20extract%20the%20core%20problem%2C%20method%2C%20results%2C%20and%20limitations%20into%20a%20structured%20intermediate%20form%2C%20then%20generate%20a%20two-host%20dialogue%20script%20where%20Host%20A%20asks%20generalist%20questions%20and%20Host%20B%20answers%20as%20the%20domain%20expert.%20Synthesize%20each%20host%27s%20lines%20with%20distinct%20ElevenLabs%20voices%2C%20mix%20background%20music%20at%20-20dB%2C%20and%20assemble%20a%20finished%20MP3%20with%20ID3%20metadata." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the project structure and core implementation from that. From there you iterate — ask it to add the math-to-speech converter for common ML notation patterns, build the batch mode that accepts a text file of arxiv IDs and generates episodes sequentially, or add an RSS feed generator so the output directory becomes a subscribable podcast feed. Each request builds on what's already there without re-explaining the context.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/arxiv-paper-to-podcast.git
cd arxiv-paper-to-podcast
pip install -r requirements.txt
pip install -e .
arxiv-podcast 1706.03762
```

The finished episode is written to `./output/1706.03762.mp3` with paper title, authors, and arxiv ID in the ID3 tags. Use `--dialogue-only` to generate the script without an ElevenLabs key.

NEO built a complete arxiv-to-podcast pipeline that turns the fire hose of ML research into something you can actually keep up with. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
