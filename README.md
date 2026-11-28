# Robin — AI-assisted dark-web OSINT investigations

**A Streamlit workbench that refines a query, searches Tor-indexed sites through multiple engines, filters the results and produces a sourced investigation summary.**

> **Provenance.** This public repository is a restored snapshot of the upstream [apurvsinghgautam/robin](https://github.com/apurvsinghgautam/robin) project by **Apurv Singh Gautam**. The application, design and documentation are that author's work, **not original work by this account**; MIT © 2025 Apurv Singh Gautam, preserved in [LICENSE](LICENSE). Badges in the original README pointed to the upstream CI, releases and Docker image; they are not claims about this mirror and have been omitted here.

## How it works

Robin separates the investigation pipeline into three parts visible in the source:

- **Search** (`search.py`) queries a list of Tor-indexed search engines through a local SOCKS proxy at `127.0.0.1:9050`, parses `.onion` result links and deduplicates them.
- **LLM layer** (`llm.py`, `llm_utils.py`) refines the user's question, filters results for relevance and writes a structured summary with a strict-grounding preset.
- **Web UI** (`ui.py`) is a Streamlit app that orchestrates the run, shows sources and findings, saves investigations to `investigations/`, and supports follow-up questions grounded in the saved investigation data.

![Robin UI](.github/assets/screen-ui.png)

## Features

- Modular search / scrape / LLM workflow, with parallel engine queries
- Model choice across OpenAI, Anthropic, Gemini, Ollama, OpenRouter, llama.cpp and any OpenAI-compatible endpoint entered in the **Custom API Provider** sidebar
- Streamlit interface with provider health checks and a dossier-style investigation view
- Saved investigations with a **Past Investigations** panel; reload a run and ask grounded follow-up questions without re-searching
- Suggested one-click pivots that start a fresh investigation from a finding
- Markdown-ready notes, findings and source lists for reporting
- Docker image and Compose-friendly deployment inherited from upstream (`apurvsg/robin`); development mode runs directly from Python

![Workflow](.github/assets/robin-workflow.png)

## Installation

Tor must be installed and running before you start; Robin uses the SOCKS port `9050` on localhost.

```bash
# Docker (upstream image)
docker pull apurvsg/robin:latest
docker run --rm \
  -v "$(pwd)/.env:/app/.env" \
  --add-host=host.docker.internal:host-gateway \
  -p 8501:8501 \
  apurvsg/robin:latest
```

Mount `$(pwd)/investigations:/app/investigations` as well to keep saved investigations across restarts. Open `http://localhost:8501`.

For development with Python 3.10+:

```bash
git clone https://github.com/anya12forger12-max/robin.git
cd robin
cp .env.example .env       # fill in only the provider keys you will use; never commit .env
pip install -r requirements.txt
streamlit run ui.py
```

`.env.example` contains placeholder names only. For Ollama, use `http://127.0.0.1:11434` locally or `http://host.docker.internal:11434` from Docker; custom OpenAI-compatible providers can be configured in the sidebar without editing `.env`.

## Responsible use

This tool is for **lawful, authorised OSINT and education only**. Accessing or interacting with some dark-web content is illegal in some jurisdictions, and information gathering can itself be regulated. Do not investigate people, systems or organisations without a legitimate basis and applicable permissions. Queries and results are sent to third-party LLM providers when a hosted model is selected — review their terms and avoid sensitive data. See the upstream disclaimer for the author's full position.

## Credits and license

Upstream project: [github.com/apurvsinghgautam/robin](https://github.com/apurvsinghgautam/robin), © 2025 Apurv Singh Gautam, [MIT licensed](LICENSE). Upstream acknowledgements: idea inspiration from [Thomas Roccia](https://x.com/fr0gger_) and his Perplexity-of-the-Dark-Web demo; the [dark-web OSINT tools](https://github.com/apurvsinghgautam/dark-web-osint-tools) list; prompt ideas from [OSINT-Assistant](https://github.com/AXRoux/OSINT-Assistant); logo by [Tanishq Rupaal](https://github.com/Tanq16/). This snapshot preserves those credits and claims no original authorship.
