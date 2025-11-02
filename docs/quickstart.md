# Quickstart

Get Etymo Agent running in under 5 minutes.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/):

=== "macOS/Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "Homebrew"

    ```bash
    brew install uv
    ```

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Rifushigi/etymo.git
    cd etymo
    ```

2. **Install dependencies**

    ```bash
    uv sync
    ```

    !!! info "What does `uv sync` do?"
        `uv sync` creates a virtual environment and installs all dependencies from `pyproject.toml` in one command. No need for `pip install -r requirements.txt`.

3. **Set up environment variables**

    ```bash
    cp .env.example .env
    ```

    Edit `.env` with your API key:

    ```env
    OPENAI_API_KEY=sk-your-key-here
    ```

## Run the Agent

Start the development server:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Test the Agent

### Method 1: Web Browser

Visit `http://localhost:8000/docs` to see the interactive API documentation (Swagger UI).

### Method 2: curl

```bash
curl -X POST http://localhost:8000/ \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": 1,
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "robot"}],
        "kind": "message"
      }
    }
  }'
```

**Expected response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "role": "agent",
    "parts": [{
      "kind": "text",
      "text": "Robot comes from Czech 'robota' meaning 'forced labor' or 'drudgery'..."
    }],
    "kind": "message",
    "messageId": "..."
  }
}
```

### Method 3: Python Client

```python
import httpx

response = httpx.post(
    "http://localhost:8000/",
    json={
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": 1,
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "philosophy"}],
                "kind": "message"
            }
        }
    }
)

result = response.json()
etymology = result["result"]["parts"][0]["text"]
print(etymology)
```

## Verify Agent Card

Check the agent metadata:

``` bash
    curl http://localhost:8000/.well-known/agent.json | jq
```

You should see the agent's capabilities, skills, and examples.

## Next Steps

- **Explore the API**: Read the [API Reference](api.md)
- **See more examples**: Check out [Examples](examples.md)

## Troubleshooting

??? question "Port 8000 already in use?"
    Change the port number:
    ```bash
    uv run uvicorn app.main:app --reload --port 8001
    ```

??? question "Module not found errors?"
    Make sure you ran `uv sync` first:
    ```bash
    uv sync
    ```

??? question "API key errors?"
    Verify your `.env` file contains valid API keys:
    ```bash
    cat .env
    ```

??? question "Connection refused?"
    Check if the server is running:

        lsof -i :8000  # macOS/Linux
        netstat -ano | findstr :8000  # Windows
