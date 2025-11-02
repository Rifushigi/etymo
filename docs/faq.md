# FAQ

Frequently asked questions about Etymo Agent.

## General Questions

### What is Etymo Agent?

Etymo Agent is an AI-powered etymology agent that provides word origins, historical context, and meaning evolution through a standardized JSON-RPC API following the Telex A2A protocol.

### Why use the A2A protocol?

The A2A protocol enables standardized agent-to-agent communication, making it easy for other systems to discover and integrate with your agent. It provides:

- Automatic discovery via `/.well-known/agent.json`
- Standardized request/response format
- Clear capability declaration
- Cross-platform compatibility

### Is it free to use?

The Etymo Agent code is open source, but you'll need:

- An API key from OpenAI, Anthropic, or run a local LLM
- Hosting infrastructure (free tier available on Railway, Fly.io, etc.)

### Can I use it commercially?

Yes! The code is MIT licensed. Check your LLM provider's terms for commercial API usage.

## Installation & Setup

### Why use `uv` instead of `pip`?

`uv` is significantly faster than `pip` and handles virtual environments automatically. Benefits:

- 10-100x faster than pip
- Automatic virtual environment management
- Better dependency resolution
- Built-in tooling support

You can still use pip if you prefer, but uv is recommended.

### Do I need to install Python first?

Yes, you need Python 3.10 or higher. `uv` doesn't include Python itself, just manages packages and environments.

```bash
# Check Python version
python3 --version  # Should be 3.10+
```

### Can I use this without an API key?

Yes, if you run a local LLM with Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Configure agent
echo "OPENAI_API_BASE=http://localhost:11434/v1" >> .env
echo "OPENAI_API_KEY=ollama" >> .env
echo "LLM_MODEL=llama3.2" >> .env
```

### Installation fails with "command not found: uv"

Install uv first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.cargo/bin:$PATH"
```

### How do I update dependencies?

```bash
# Update all packages
uv sync --upgrade

# Update specific package
uv add fastapi@latest
```

## API & Usage

### What's the difference between this and a dictionary API?

Traditional dictionary APIs return definitions. Etymo Agent provides:

- Historical word origins
- Language family connections
- Meaning evolution over time
- Cultural and historical context
- LLM-powered insights

### Can I look up phrases or multiple words?

Currently optimized for single word lookups. For phrases, the agent will provide etymology for the overall phrase if applicable, or break it down into components.

### How accurate are the etymologies?

Accuracy depends on the LLM model used:

- **GPT-4o/Claude 3.5**: Generally very accurate for common words
- **GPT-4o-mini/Claude 3.5 Haiku**: Good accuracy, occasionally simplified
- **Local models**: Variable accuracy, may hallucinate for rare words

Always verify critical etymological information with academic sources.

### Can I customize the response format?

Yes! Edit the system prompt in `app/llm.py`:

```python
SYSTEM_PROMPT = """You are an expert etymologist.
Provide etymology in this format:
- Origin: [language and root]
- Meaning: [literal translation]
- First Use: [time period]
- Evolution: [how meaning changed]
"""
```

### Does it support languages other than English?

The agent can provide etymologies for words in any language, but:

- Prompts and responses are in English by default
- Quality depends on the LLM's training data
- Modify system prompt to support other response languages

```python
SYSTEM_PROMPT = """You are an expert etymologist.
Provide responses in Spanish."""
```

## Documentation

### Can I customize the docs theme?

Yes you can, edit `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: deep-purple  # Change color
    accent: amber
  logo: assets/logo.png  # Add logo
  favicon: assets/favicon.png
```

See [MkDocs Material documentation](https://squidfunk.github.io/mkdocs-material/) for more options.

## Troubleshooting

### "No module named 'app'" error

Make sure you're running from the project root:

```bash
cd /path/to/etymo
uv run uvicorn app.main:app
```

### Port 8000 already in use

Change the port:

```bash
uv run uvicorn app.main:app --port 8001
```

### API returns errors for all requests

Check your API key:

```bash
# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Common issues:

- Invalid API key
- Insufficient credits
- Rate limit exceeded
- Wrong base URL

### Responses are too long/short

Adjust max tokens in `.env`:

```env
LLM_MAX_TOKENS=300  # Shorter responses
LLM_MAX_TOKENS=800  # Longer responses
```

Or modify the system prompt to control length.

### Docker build fails

Try clearing cache:

```bash
docker build --no-cache -t etymo .
```

Or use multi-stage build for better caching.

### MkDocs serve shows 404 errors

Rebuild the nav structure:

```bash
rm -rf site/
uv tool run mkdocs build
uv tool run mkdocs serve
```

### Agent doesn't start on VPS

Check logs:

```bash
# Systemd logs
sudo journalctl -u etymo -n 100 -f

# Check service status
sudo systemctl status etymo

# Test manually
cd /opt/etymo
uv run uvicorn app.main:app
```

## Performance

### How fast are responses?

Typical response times:

- **GPT-4o-mini**: 1-3 seconds
- **GPT-4o**: 2-4 seconds
- **Claude 3.5 Haiku**: 1-2 seconds
- **Claude 3.5 Sonnet**: 2-5 seconds
- **Local Ollama**: 5-30 seconds (hardware dependent)

### Can I cache responses?

Yes! Add Redis or in-memory caching:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_etymology(word: str) -> str:
    # ... LLM call
```

Or use Redis for persistent cache across restarts.

## Customization

### Can I add more skills?

Yes! Add new skills to agent card:

```python
# app/agent_card.py
{
    "id": "related-words",
    "name": "Find Related Words",
    "description": "Find words with similar etymology",
    # ...
}
```

Then implement the logic in `app/main.py`.

### Can I use different LLM providers?

Yes! Supported out of the box:

- OpenAI (GPT models)
- Anthropic (Claude models)
- Any OpenAI-compatible API (Ollama, Together AI, etc.)

Add support for others by modifying `app/llm.py`.

### Can I modify the response format?

Yes you can... Edit the system prompt to change:

- Verbosity level
- Structure (bullet points, paragraphs, JSON)
- Focus areas (academic vs casual)
- Additional information (cognates, usage examples)

### Can I add authentication?

Yes, add API key authentication:

```python
# app/middleware.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")

# app/main.py
@app.post("/", dependencies=[Depends(verify_api_key)])
async def handle_request():
    # ... handle request
```

## Contributing

### How can I contribute?

We welcome contributions! Areas that need help:

- Additional LLM provider support
- Response caching
- Rate limiting improvements
- Test coverage
- Documentation examples
- Multi-language support

### Where do I report bugs?

Open an issue on [GitHub Issues](https://github.com/Rifushigi/etymo/issues) with:

- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, uv version)
- Logs or error messages

### Can I request features?

Yes! Open a [feature request](https://github.com/Rifushigi/etymo/issues/new?template=feature_request.md) or start a [discussion](https://github.com/Rifushigi/etymo/discussions).

## Still Have Questions?

- **Check the docs**: [Full documentation](index.md)
- **Ask on GitHub**: [Discussions](https://github.com/Rifushigi/etymo/discussions)
- **Report issues**: [GitHub Issues](https://github.com/Rifushigi/etymo/issues)