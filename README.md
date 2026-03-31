\# Financial Assistant AI Agent



An AI-powered financial assistant with multi-agent architecture and guardrails built using Google Gemini and Python.



\## Features

\- Real-time stock price fetching via yfinance

\- Investment reasoning with chain-of-thought

\- Portfolio analysis

\- Financial news retrieval

\- Multi-agent system: Planner → Executor → Critic

\- 3-layer guardrail system



\## Guardrails

| Type | What it does |

|------|-------------|

| Input | Blocks prompt injection, harmful queries, off-topic requests |

| Output | Blocks misleading guarantees, hallucinations, unsafe claims |

| Behavioral | Restricts agent to finance domain only |



\## Architecture

User → Input Guardrail → Planner Agent → Executor Agent (Tools) → Critic Agent → Output Guardrail → Response



\## Setup Instructions



\### Prerequisites

\- Python 3.10+

\- Google Gemini API key (free at aistudio.google.com)



\### Installation

```bash

git clone <your-repo-url>

cd financial-assistant

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



\### Configuration

Create a `.env` file:

```

GEMINI\_API\_KEY=your\_key\_here

```



\### Run

```bash

python -m src.main

```



\### Run Tests

```bash

python evaluation/test\_cases.py

```



\## Example Queries

\- "What is the price of AAPL?"

\- "Should I invest in NVDA?"

\- "Show me my portfolio"

\- "If I bought 10 shares of TSLA at $200 and now it is $250 what is my profit?"



\## Tech Stack

\- Python 3.10

\- Google Gemini 2.5 Flash

\- yfinance

\- LangChain

\- python-dotenv

