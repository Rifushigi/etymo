# Agent Card

The agent card (`/.well-known/agent.json`) provides metadata about Etymo Agent's capabilities for Telex A2A protocol discovery.

## Overview

The agent card is a standardized JSON document that describes:

- Agent identity and version
- Supported capabilities
- Available skills and examples
- Input/output modes
- Provider information

## Access the Agent Card

```bash
curl http://localhost:8000/.well-known/agent.json | jq
```

## Full Agent Card Schema

```json
{
  "name": "EtymoAgent",
  "description": "AI-powered etymology agent that returns word origins, historical context, and meaning evolution.",
  "url": "https://agent-domain.com",
  "version": "1.0.0",
  "provider": {
    "organization": "rifushigi",
    "url": "https://agent-domain.com",
    "email": "support@your-agent-domain.com"
  },
  "documentationUrl": "https://agent-domain.com/docs",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "stateTransitionHistory": false,
    "contextWindow": 4096
  },
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain"],
  "authentication": {
    "required": false,
    "methods": []
  },
  "skills": [
    {
      "id": "etymology-lookup",
      "name": "Etymology Lookup",
      "description": "Given a word or phrase, returns its etymology including origin language, root words, historical context, and meaning evolution.",
      "inputModes": ["text/plain"],
      "outputModes": ["text/plain"],
      "parameters": {
        "word": {
          "type": "string",
          "description": "The word to look up",
          "required": true
        }
      },
      "examples": [
        {
          "input": {
            "parts": [
              {
                "kind": "text",
                "text": "philosophy"
              }
            ]
          },
          "output": {
            "parts": [
              {
                "kind": "text",
                "text": "Philosophy comes from Greek 'philosophia' (φιλοσοφία), combining 'philo-' (loving) and 'sophia' (wisdom). First used in English in the 14th century via Old French 'philosophie'. Originally referred to the study of fundamental nature of knowledge and reality."
              }
            ]
          }
        },
        {
          "input": {
            "parts": [
              {
                "kind": "text",
                "text": "robot"
              }
            ]
          },
          "output": {
            "parts": [
              {
                "kind": "text",
                "text": "Robot comes from Czech 'robota' meaning 'forced labor' or 'drudgery', from 'rab' (slave). Coined by Karel Čapek in his 1920 play 'R.U.R.' (Rossum's Universal Robots). The word quickly entered English and other languages to describe artificial workers."
              }
            ]
          }
        },
        {
          "input": {
            "parts": [
              {
                "kind": "text",
                "text": "serendipity"
              }
            ]
          },
          "output": {
            "parts": [
              {
                "kind": "text",
                "text": "Serendipity was coined by Horace Walpole in 1754, inspired by the Persian fairy tale 'The Three Princes of Serendip' (Sri Lanka). The princes made fortunate discoveries by accident. Combines 'Serendip' (old name for Sri Lanka) with '-ity' suffix, meaning the faculty of making happy and unexpected discoveries."
              }
            ]
          }
        }
      ]
    }
  ],
  "supportedProtocols": ["a2a-v1"],
  "supportsAuthenticatedExtendedCard": false,
  "metadata": {
    "tags": ["etymology", "linguistics", "education", "language"],
    "categories": ["education", "reference", "language-tools"],
    "languages": ["en"],
    "license": "MIT"
  }
}
```

## Field Reference

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable agent name |
| `description` | string | Yes | Brief description of agent's purpose |
| `url` | string | Yes | Base URL where agent is hosted |
| `version` | string | Yes | Semantic version (e.g., "1.0.0") |
| `documentationUrl` | string | No | Link to full documentation |

### Provider Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization` | string | Yes | Organization name |
| `url` | string | No | Organization website |
| `email` | string | No | Support contact email |

### Capabilities Object

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `streaming` | boolean | false | Supports streaming responses |
| `pushNotifications` | boolean | false | Can send push notifications |
| `stateTransitionHistory` | boolean | false | Maintains conversation state |
| `contextWindow` | number | N/A | Maximum context size in tokens |

### Skills Array

Each skill represents a specific capability:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique skill identifier |
| `name` | string | Yes | Human-readable skill name |
| `description` | string | Yes | Detailed skill description |
| `inputModes` | array | Yes | Supported input MIME types |
| `outputModes` | array | Yes | Supported output MIME types |
| `parameters` | object | No | Skill parameters schema |
| `examples` | array | No | Example input/output pairs |

### Authentication Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `required` | boolean | Yes | Whether auth is required |
| `methods` | array | No | Supported auth methods (e.g., ["bearer", "oauth2"]) |

## Validation

### Test Agent Card Format

```bash
# Fetch and validate JSON
curl http://localhost:8000/.well-known/agent.json | jq . > /dev/null
echo "Agent card is valid JSON"
```

### Python Validation

```python
import httpx
from pydantic import BaseModel, HttpUrl

class AgentCard(BaseModel):
    name: str
    description: str
    url: HttpUrl
    version: str

# Validate
response = httpx.get("http://localhost:8000/.well-known/agent.json")
card = AgentCard(**response.json())
print(f"Agent card valid: {card.name} v{card.version}")
```

## Next Steps

- See [API Reference](api.md) for endpoint details