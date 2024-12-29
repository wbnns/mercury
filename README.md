# Mercury

![Alt](https://repobeats.axiom.co/api/embed/9544f667a7bd12b1a14ca45000e1f5cc7d2d4d45.svg "Mercury")

## Overview

Mercury automates GitHub and Notion interactions, summarizing activity for the past week and posting it to a Notion workspace.

## Features

- Fetches GitHub PRs, Issues, and Gists.
- Posts weekly summaries to a Notion page.

## Setup

1. Clone the repository.
2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Set up the page you want to post to in Notion
4. Configure your `.env` file based on `.env.example`.

## Usage

`python main.py`

## License

MIT
