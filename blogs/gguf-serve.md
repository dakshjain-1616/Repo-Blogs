---
title: "gguf-serve — OpenAI-Compatible Local Inference Server for GGUF Models"
description: "NEO built gguf-serve, a Flask-based server that exposes any GGUF model through OpenAI-compatible endpoints with zero configuration and a built-in mock mode."
date: 2026-03-28
tags: [gguf, llama-cpp, openai-api, local-inference, flask]
slug: gguf-serve
github: https://github.com/dakshjain-1616/gguf-serve
---

# gguf-serve — OpenAI-Compatible Local Inference Server for GGUF Models

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/gguf-serve)

![Pipeline Architecture](../public/images/diagrams/gguf-serve.png)

## The Problem

> Running a GGUF model locally usually means writing custom inference code or wrestling with llama.cpp's CLI flags every time you want to test something. Existing OpenAI-compatible servers often require Docker, complex configuration files, or GPU support. The gap between "I have a .gguf file" and "I have a working API endpoint" is wider than it should be.

NEO built gguf-serve to close that gap with a single Python file. Point it at any `.gguf` file, run the server, and immediately get OpenAI-compatible endpoints that work with any client library or tool that speaks the OpenAI API format.

## OpenAI-Compatible Endpoints

**gguf-serve** exposes two endpoints that match the OpenAI API specification:

- `POST /v1/completions` for text completion
- `POST /v1/chat/completions` for chat-style conversations

The request and response formats are wire-compatible with OpenAI's API. This means you can swap out `api.openai.com` for `localhost:PORT` in any existing codebase and the client library won't notice the difference. Tools like LangChain, LiteLLM, and raw `openai` Python SDK all work without modification.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="unused")
response = client.chat.completions.create(
    model="local",
    messages=[{"role": "user", "content": "Explain quantization in one paragraph."}]
)
print(response.choices[0].message.content)
```

## Mock Mode for Integration Testing

One of the most practical features is **mock mode**. Starting the server with `--mock` loads a lightweight stub instead of an actual model. The stub returns realistic-looking responses with correct JSON structure, proper token counts, and valid finish reasons.

This is useful for integration testing: you can verify that your application correctly parses responses, handles streaming, and manages errors without downloading a multi-gigabyte model or needing a GPU. CI pipelines can run against mock mode to test the full request path.

```bash
python server.py --mock --port 8080
```

Mock mode produces responses immediately, with no latency from actual inference, which also makes it useful for load-testing request handling logic.

## Pure Python, No Docker

The server is implemented in Flask, which means it runs in any Python 3.8+ environment without Docker, without CUDA drivers, and without native dependencies beyond llama-cpp-python. The Flask layer is thin: it validates the incoming JSON, calls the model inference function, and formats the output to match OpenAI's response structure.

Because the code is plain Python, debugging is straightforward. You can add breakpoints, print intermediate values, and trace exactly what happens between the HTTP request and the model call. Contrast this with compiled servers where the inference path is opaque.

Port customization prevents conflicts when you are running multiple services locally:

```bash
python server.py --model ./llama-3-8b-q4.gguf --port 9090
```

## Streaming Support

For long completions, **token streaming** sends each generated token as a server-sent event as soon as it is available, rather than waiting for the entire response. This is the same mechanism OpenAI's streaming API uses, and clients that support it get much lower time-to-first-token.

Streaming is optional and controlled by the `stream` field in the request body. Non-streaming clients get the complete response in one JSON object, identical to the OpenAI non-streaming format.

## How to Build This

Clone the repo and install dependencies:

```bash
git clone https://github.com/dakshjain-1616/gguf-serve
cd gguf-serve
pip install -r requirements.txt
```

Start the server against a local GGUF file:

```bash
python server.py --model ./your-model.gguf --port 8080
```

Or start in mock mode without any model file:

```bash
python server.py --mock --port 8080
```

Send a chat completion request:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

For streaming responses, add `"stream": true` to the request body. The server will return server-sent events with `data:` prefixed JSON chunks.

Run the test suite:

```bash
pytest tests/ -v
# 42 passed
```

The 42-test suite covers endpoint validation, response format compliance, mock mode behavior, error handling, and streaming correctness.

NEO built gguf-serve as a minimal, debuggable OpenAI-compatible server that exposes any GGUF model as a local API endpoint with zero configuration overhead. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
