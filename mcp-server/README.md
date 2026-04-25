# StoryVault — MCP Server

Python MCP server that gives Claude tools to interact with the StoryVault backend and coach writing sessions.

## Stack

- **mcp** — Model Context Protocol server (FastMCP)
- **httpx** — HTTP client for StoryVault API calls
- **python-dotenv** — environment config

## Tools

| Tool | Description |
|------|-------------|
| `get_writing_challenge` | Generate a challenge using provided vocab words |
| `get_template` | Return a writing structure template for a category |
| `coach_writing` | Feedback on hook, structure, flow, and vocab usage |
| `check_vocabulary` | Check which words are used → `{used, missing, score}` |
| `save_journal` | POST a journal entry to StoryVault |
| `save_story` | POST a polished story to StoryVault |
| `get_stories` | Fetch stories, optional category filter |
| `get_journals` | Fetch journals, optional category + limit |
| `get_stats` | Fetch writing stats for today |

## Setup

```bash
python -m venv venv && venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your StoryVault backend URL
```

## Environment variables

```
API_URL=http://192.168.1.224:8001
```

## Run

```bash
python src/index.py
```

The server communicates over **stdio** — it blocks waiting for MCP client input. No HTTP port is opened.

## Claude Desktop config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "storyvault": {
      "command": "python",
      "args": ["C:/path/to/StoryVault/mcp-server/src/index.py"],
      "env": {
        "API_URL": "http://192.168.1.224:8001"
      }
    }
  }
}
```
