---
title: "Videoseek CLI: Semantic Search Across Video Content With Timestamp Precision"
description: "NEO built Videoseek CLI, a command-line tool for natural language search over video content that transcribes, embeds, and indexes video audio to return timestamp-accurate results for any query."
date: 2026-03-23
tags: [video search, semantic search, embeddings, transcription, CLI, NLP]
slug: videoseek-cli
github: https://github.com/dakshjain-1616/videoseek-cli
---

# Videoseek CLI: Semantic Search Across Video Content With Timestamp Precision

[![View on GitHub](https://img.shields.io/badge/View_on_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakshjain-1616/videoseek-cli)

![Pipeline Architecture](../public/images/diagrams/videoseek-cli.png)

## The Problem

> Long-form video is a knowledge silo. A two-hour conference talk, a recorded architecture review, a weekly all-hands recording — they all contain valuable information that is completely unsearchable. You cannot Ctrl+F a video. You either watch the whole thing, scrub through hoping to find the right moment, or rely on whoever wrote the description to have mentioned the topic you care about. None of these scale.

NEO built Videoseek CLI to make video as searchable as text. Transcribe once, then ask natural language questions and get back the exact timestamps where the answer lives.

## Transcription Pipeline

The first stage converts audio to text. Videoseek CLI supports two input types: YouTube URLs (the tool downloads the audio track using yt-dlp) and local video files in any format that ffmpeg can decode (mp4, mkv, webm, mov, avi, and more).

Audio extraction strips the video track and produces a mono 16kHz WAV, which is the standard input format for speech recognition models. Transcription runs through Whisper — either OpenAI's API or a local model (tiny, base, small, medium, large) depending on your configuration. For most use cases, the `small` model running locally provides an excellent balance of speed and accuracy. The `large` model is available for content with heavy technical jargon, non-standard accents, or low audio quality.

Whisper's output is word-level timestamped text: every word in the transcript carries a start time and end time in seconds. Videoseek CLI preserves this granularity throughout the pipeline. The final search results will point to a specific second in the video, not a vague "somewhere around 45 minutes."

The raw transcript is segmented into chunks for embedding. Each chunk is a semantically coherent passage — typically 3-5 sentences or 30-60 seconds of speech, whichever boundary comes first. Chunking at sentence boundaries rather than fixed time windows is important: a fixed 30-second window might split a sentence mid-thought, degrading the coherence of the embedded passage and reducing retrieval accuracy.

## Embedding and Indexing

Each transcript chunk is embedded using a sentence-level embedding model. The default is `text-embedding-3-small` from OpenAI, which provides strong semantic representations at low cost. The tool also supports local embedding models via sentence-transformers (all-MiniLM-L6-v2, all-mpnet-base-v2) for fully offline operation.

The embedding for each chunk is stored in a vector index alongside its metadata: the source video identifier, the start timestamp in seconds, the end timestamp in seconds, the chunk text, and the speaker label if speaker diarization was run. The vector index defaults to FAISS (in-memory, fast, no external dependencies). For persistent indexes that survive process restarts and support incremental addition of new videos, a ChromaDB backend is available.

Indexing a two-hour video with the `small` Whisper model and local embeddings takes roughly 4-8 minutes on a modern CPU, or 1-2 minutes with a GPU. The resulting index is a few megabytes — small enough to commit to a repository or attach to a project directory.

## Semantic Search

The query interface is a single command: `videoseek search "the part where they discuss deployment architecture"`. The query string is embedded using the same model used during indexing, and the embedding is compared to all chunk embeddings in the index using cosine similarity. The top-k most similar chunks are returned as results.

Each result includes the timestamp as both a human-readable string (`1:23:47`) and a raw second count, the similarity score, and the chunk text. For YouTube videos, the result also includes a direct URL with a `?t=` parameter that jumps to the exact moment.

The semantic nature of the search means queries do not need to use the exact words spoken in the video. "How did they handle database migrations" will match a passage where someone talks about "schema changes" and "running Alembic on deploy." The embedding captures meaning, not surface form. This is the key difference from transcript text search, which would miss synonyms and paraphrases.

Hybrid search is available as an option: the tool runs both semantic search and BM25 keyword search on the transcript text, then merges the results using reciprocal rank fusion. Hybrid search outperforms pure semantic search for queries that contain specific technical terms, proper nouns, or exact phrases — cases where the semantic embedding might spread similarity across many loosely related passages.

## Multi-Video Collections

Videoseek CLI supports indexing multiple videos into a shared collection. After indexing several videos, a search query returns results from across the entire collection, each result tagged with its source video.

This is the feature that makes Videoseek genuinely useful for knowledge management. Index all recordings from a conference track, all episodes of a technical podcast, or all onboarding videos for a new team member. Then search the entire collection with a single query. "What did the speakers say about rate limiting" returns the best matches from any video in the collection, with timestamps pointing to the exact moment in the right video.

Collection metadata is stored in a lightweight SQLite database alongside the vector index. Adding a new video to an existing collection is incremental — only the new video is transcribed and embedded; the existing index is not rebuilt.

## Speaker Diarization

An optional speaker diarization step labels each transcript segment with a speaker identifier (Speaker 1, Speaker 2, etc.) using pyannote.audio. When diarization is enabled, search results include the speaker label for each matching chunk.

This adds a useful filter dimension: `videoseek search "deployment concerns" --speaker "Speaker 2"` restricts results to segments where the second identified speaker is talking. In a recorded meeting with known participants, you can map speaker labels to names after diarization and search by speaker name.

## CLI Interface and Output Formats

Videoseek CLI is driven by three commands. `videoseek index <source>` transcribes and indexes a video or URL. `videoseek search <query>` searches the current collection. `videoseek list` shows all indexed videos with their duration and chunk count.

Output defaults to a human-readable table in the terminal. The `--json` flag emits structured JSON for piping into other tools. The `--open` flag on macOS and Linux attempts to open the video at the matching timestamp directly in the default media player or browser.

## How to Build This with NEO

Open NEO in VS Code or Cursor and describe what you want to build. A good starting prompt for this project:

> "Build a Python CLI tool called videoseek with three commands: index, search, and list. The index command accepts a YouTube URL or local video file, extracts audio with yt-dlp/ffmpeg, transcribes with Whisper (local or API), segments the transcript at sentence boundaries into 30-60 second chunks preserving word-level timestamps, embeds each chunk with text-embedding-3-small or local sentence-transformers, and stores embeddings in a FAISS or ChromaDB index with source video metadata. The search command embeds a query and returns top-k results with timestamps, similarity scores, and direct YouTube ?t= URLs. Support multi-video collections in a SQLite metadata store."

<a href="https://heyneo.so/dashboard?section=new-chat&prompt=Build%20a%20Python%20CLI%20tool%20called%20videoseek%20with%20three%20commands%3A%20index%2C%20search%2C%20and%20list.%20The%20index%20command%20accepts%20a%20YouTube%20URL%20or%20local%20video%20file%2C%20extracts%20audio%20with%20yt-dlp%2Fffmpeg%2C%20transcribes%20with%20Whisper%20%28local%20or%20API%29%2C%20segments%20the%20transcript%20at%20sentence%20boundaries%20into%2030-60%20second%20chunks%20preserving%20word-level%20timestamps%2C%20embeds%20each%20chunk%20with%20text-embedding-3-small%20or%20local%20sentence-transformers%2C%20and%20stores%20embeddings%20in%20a%20FAISS%20or%20ChromaDB%20index%20with%20source%20video%20metadata.%20The%20search%20command%20embeds%20a%20query%20and%20returns%20top-k%20results%20with%20timestamps%2C%20similarity%20scores%2C%20and%20direct%20YouTube%20%3Ft%3D%20URLs.%20Support%20multi-video%20collections%20in%20a%20SQLite%20metadata%20store." style="display:inline-block;background:#1e40af;color:#ffffff;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:14px;">Build with NEO →</a>

NEO generates the transcription pipeline, embedding and indexing logic, multi-video collection management, and CLI interface. From there you iterate -- ask it to add hybrid BM25 + semantic search with reciprocal rank fusion for better technical term matching, add optional speaker diarization using pyannote.audio with a `--speaker` search filter, or add a `--json` output flag for piping results into other tools.

To run the finished project:

```bash
git clone https://github.com/dakshjain-1616/videoseek-cli
cd videoseek-cli
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
videoseek index https://www.youtube.com/watch?v=dQw4w9WgXcQ
videoseek search "database migration strategy"
```

Results show timestamps, similarity scores, and direct `?t=` URLs -- every video you index becomes searchable in natural language with second-level precision.

NEO built Videoseek CLI so that long-form video stops being a knowledge silo -- one index command and every recording in your collection becomes instantly searchable with timestamp-accurate results. See what else NEO ships at [heyneo.so](https://heyneo.so/).

---

## Try NEO in Your IDE

Install the NEO extension to bring AI-powered development directly into your workflow:

- **VS Code**: [NEO in VS Code](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
- **Cursor**: <a href="cursor://extension/NeoResearchInc.heyneo" style="color:#0066FF;font-weight:bold;">Install NEO for Cursor →</a>

---
