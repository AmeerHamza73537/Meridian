# Meridian

**An autonomous multi-agent AI research system built with LangChain.**

It is a MultiAgent Research Assistant, a fully autonomous AI system that thinks, searches, reads and writes on its own. Instead of a single AI answering your question from memory, we are deploying a team of specialized intelligent agents that collaborate together to produce a professional research report on any topic you give them.

1. The **Search Agent** goes out on the live internet and finds the most relevant and recent resources.
2. The **Reader Agent** then dives deep into the sources, scraping and extracting meaningful content.
3. The **Writer Agent** takes all that gathered intelligence and crafts a well-structured, detailed report.
4. Finally, the **Critic Agent** reviews the entire report, scores it and gives feedback like a senior researcher reviewing a junior's work.

Every single agent is powered by an LLM, connected through LangChain's modern LCEL pipeline, and orchestrated through a shared memory system that makes them work as one unified brain.

> This is not a chatbot. This is not a simple Q&A tool. This is a production-level agentic AI system — the kind of architecture that top AI companies are actively building and hiring for right now.

---

## How it works

```
Research Topic
      │
      ▼
┌─────────────────┐      Tavily API
│  Search Agent    │ ───► finds recent, relevant sources
└─────────────────┘
      │
      ▼
┌─────────────────┐      BeautifulSoup
│  Reader Agent     │ ───► scrapes & extracts deep content
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Writer Chain     │ ───► drafts the full structured report
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Critic Chain     │ ───► scores the report & gives feedback
└─────────────────┘
      │
      ▼
  Final Report + Critique
```

---

## Features

- **Fully autonomous pipeline** — give it a topic, get a finished, reviewed report with zero manual steps in between.
- **Real, live research** — the Search Agent pulls current information from the web via the Tavily API instead of relying on the model's memory.
- **Deep content extraction** — the Reader Agent scrapes and cleans the most relevant source for detail, not just headlines and snippets.
- **Structured report writing** — the Writer Chain outputs a report with a clear Introduction, Key Findings, Conclusion, and Sources section.
- **Built-in quality control** — the Critic Chain independently scores the report out of 10 and lists concrete strengths and areas to improve.
- **Interactive UI** — a Streamlit interface with a live pipeline tracker showing each agent's status in real time, plus a downloadable Markdown report.

---

## Tech stack

| Layer | Technology |
|---|---|
| Orchestration | LangChain (agents + LCEL pipelines) |
| LLM | Google Gemini (`gemini-flash-latest`) |
| Web search | Tavily API |
| Content scraping | BeautifulSoup + Requests |
| Frontend | Streamlit |
| Language | Python |

---

## Project structure

```
.
├── app.py          # Streamlit UI and pipeline runner
├── agents.py       # Agent + chain definitions (Search, Reader, Writer, Critic)
├── tools.py        # web_search and scrape_url tool implementations
├── pipeline.py      # Standalone CLI runner for the research pipeline
├── requirements.txt
└── .env             # API keys (not committed)
```

---

## Getting started

### Prerequisites

- Python 3.10+
- A [Tavily](https://tavily.com) API key
- A [Google AI Studio](https://aistudio.google.com) API key for Gemini

### Installation

```bash
git clone https://github.com/<your-username>/Meridian.git
cd Meridian
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Run the app

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`) and enter a research topic to kick off the pipeline.

---

## Roadmap

- [ ] Multi-source scraping (currently reads one top result per run)
- [ ] Export reports to PDF/Word in addition to Markdown
- [ ] Persistent research history
- [ ] Configurable agent models per step

---

## Author

Built by **Ameer Hamza** — MERN stack developer transitioning into AI/ML engineering.