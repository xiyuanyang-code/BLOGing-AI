# BlOGing AI: An AI-Enhanced Blog Reader

## Introduction

<!-- todo add basic info -->

## Installation

We recommend you to run **BLOGing AI** locally.

- Cloning the repository.

```bash
git clone https://github.com/xiyuanyang-code/BLOGing-AI.git
cd BLOGing-AI
```

- Installing dependecies.

```bash
# Python 3.12 is recommended
pip install -r requirements.txt
```

- Start and stop the service.

```bash
bash deploy.sh
# - The backend (Flask) will run on http://127.0.0.1:5000
# - The frontend (HTTPS) will run on https://127.0.0.1:8000

# Stop all the services
bash undeploy.sh
```

Then visit http://127.0.0.1:8000 in your browser and enjoy your learning trip!

## Usage


## Todo List

- Refactor the bash scripts to cleanly kill processes occupying the ports.

- Complete the MCP content and AI summarization features

    - fetch: Automatically crawl blog content

    - summarize: Let AI generate summaries

    - check: Check for grammatical errors and logical inconsistencies

    - mark: Structured annotation

    - extension: MCP external tools for arXiv and Wikipedia

- Make the
