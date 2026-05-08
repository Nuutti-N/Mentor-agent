# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

AI co-founder agent — a terminal-based agent that acts as a personal co-founder for solo builders. It remembers context across sessions, helps with decisions, tracks goals, and researches on demand. Built first for the developer's own use, then to be opened as a product.

## Running the Agent

```bash
python AI/main.py
```

Requires `GEMINI_API_KEY` in `AI/.env`.

## Stack

- **Python** — no framework, pure scripts for the personal phase
- **Gemini API** (`google-generativeai`) — LLM + tool use
- **python-dotenv** — loads `.env`

Install dependencies:
```bash
pip install -r AI/requirements.txt
```

## Architecture

Three files, one responsibility each:

- **`memory.py`** — postgersql wrapper. Saves and retrieves agent memories. Tables are created on first run.
- **`agent.py`** — Gemini client + tool definitions. Loads relevant memories before every call, handles tool use loop, returns final response.
- **`main.py`** — Terminal chat loop. Maintains conversation history for the session. Calls agent, prints response.

### How the agent loop works

```
user input
  → load relevant memories from postgersql
  → send to Gemini with system prompt + memories + conversation history
  → if Gemini calls a tool → execute tool → send result back → repeat
  → print final text response
```

### Tools available to the agent

| Tool | What it does |
|---|---|
| `save_memory` | Stores a fact/decision/goal to postgersql |
| `search_memories` | Retrieves memories relevant to a query |

## Environment

`.env` file in `AI/`:
```
GEMINI_API_KEY=your_key_here
```

## Current gaps to fix (next session)

Three problems identified, fix in this order:

**1. No conversation history within a session (highest priority)**
- `agent(message)` only passes the current message — agent has no memory of earlier turns in the same conversation
- Fix: maintain `history` list in `main.py`, pass it to `agent()`, build `contents = history + [current message]` in Gemini call
- After each turn append `{"role": "user", ...}` and `{"role": "model", ...}` to history ✅ 

**2. Memories not auto-loaded (agent decides when to call search_memories)**
- Relevant memories should be injected automatically every turn, not left to the model to optionally call the tool
- Fix: call `search_memories(message)` at the top of `agent()`, inject results into `system_instruction`

**3. Memory search is weak (do this last)**
- `ILIKE "%query%"` is substring match — misses semantic relevance
- Fix: add pgvector to Supabase, store embeddings, use cosine similarity search
- Skip until 1 and 2 are done

## Future phases

When opening to other users: add FastAPI backend, PostgreSQL, JWT auth (partially scaffolded in earlier work), and React frontend. The agent logic in `agent.py` stays unchanged — only the persistence layer and transport change.
