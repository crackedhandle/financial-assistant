# Architecture — Financial Assistant AI Agent

## System Overview

The Financial Assistant is built on a **multi-agent pipeline** where specialized agents handle distinct responsibilities. Every user query passes through a strict input-to-output pipeline with guardrails at both ends.

---

## Agent Roles

### 1. Planner Agent (`src/agents/planner.py`)
- Receives the raw user query
- Uses Gemini LLM to decompose it into a structured JSON execution plan
- Decides which tools are needed and in what order
- Example: "Should I invest in NVDA?" → plan to fetch stock price + news

### 2. Executor Agent (`src/agents/executor.py`)
- Receives the plan from the Planner
- Calls each tool in sequence
- Aggregates all tool results into a single context string
- No LLM calls — pure deterministic tool execution

### 3. Critic Agent (`src/agents/critic.py`)
- Receives the user query + all tool results
- Uses Gemini LLM to synthesize a coherent, factual financial response
- Enforces behavioral guardrails through its system prompt
- Always adds a disclaimer

---

## Tools

| Tool | File | Description |
|------|------|-------------|
| Stock Data | `src/tools/stock_data.py` | Fetches price, 52W range, P/E, market cap via yfinance |
| Calculator | `src/tools/calculator.py` | ROI, compound interest, Sharpe ratio |
| News Fetch | `src/tools/news_fetch.py` | Latest 5 news headlines per ticker via yfinance |
| Portfolio | `src/tools/portfolio.py` | Reads mock_portfolio.json and summarizes holdings |

---

## Guardrail Layers

```
Layer 1: Input Guardrail
  ├── Prompt injection detection (regex patterns)
  ├── Harmful keyword filter
  └── Domain restriction (finance keywords check)

Layer 2: Behavioral Guardrail (Critic system prompt)
  ├── Never guarantee returns
  ├── Always cite data sources
  ├── Always add disclaimer
  └── Use hedged language only

Layer 3: Output Guardrail
  ├── Unsafe financial promise detection
  ├── Hallucination trigger detection
  └── Response length validation
```

---

## Data Flow

```
[User] "Should I invest in NVDA?"
    │
    ▼
[Input Guard] → check_input() → allowed: True
    │
    ▼
[Planner] → Gemini API call → 
    {
      "tasks": [
        {"tool": "get_stock_price", "params": {"ticker": "NVDA"}},
        {"tool": "get_news", "params": {"ticker": "NVDA"}}
      ]
    }
    │
    ▼
[Executor] → 
    Tool 1: yfinance → NVDA price, P/E, market cap
    Tool 2: yfinance → 5 latest news headlines
    │
    ▼
[Critic] → Gemini API call with tool results →
    "Based on data: NVDA trades at $170.81...
     Consider the risks... Disclaimer..."
    │
    ▼
[Output Guard] → check_output() → safe: True
    │
    ▼
[User] receives final response
```

---

## Technology Choices

| Decision | Choice | Reason |
|----------|--------|--------|
| LLM | Google Gemini 2.5 Flash | Free tier, fast, capable reasoning |
| Stock Data | yfinance | Free, no API key needed, real-time |
| Guardrails | Custom regex + rule-based | Transparent, fast, no extra API cost |
| Agent pattern | Custom pipeline | Full control over flow and guardrails |

---

## Sequence Diagram

```
User        InputGuard    Planner      Executor     Tools      Critic     OutputGuard
 │               │            │            │           │           │            │
 │──── query ───►│            │            │           │           │            │
 │               │─ check ───►│            │           │           │            │
 │               │◄─ allow ───│            │           │           │            │
 │               │            │            │           │           │            │
 │──────────────────── query ►│            │           │           │            │
 │               │            │─── plan ──►│           │           │            │
 │               │            │            │─── call ─►│           │            │
 │               │            │            │◄── data ──│           │            │
 │               │            │            │─── results ──────────►│            │
 │               │            │            │           │           │─ response ►│
 │               │            │            │           │           │◄─ safe ────│
 │◄──────────────────────────────────────────────────── final response ─────────│
```
