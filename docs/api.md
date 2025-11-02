# API Reference

API documentation for Etymo Agent.

## Base URL

```
http://localhost:8000  # Development
https://agent.com # Production
```

## Endpoints

### Health Check

Check if the agent is running.

**Endpoint:** `GET /health`

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-02T12:34:56Z"
}
```

### Agent Metadata

Retrieve agent capabilities and skills for Telex discovery.

**Endpoint:** `GET /.well-known/agent.json`

**Response:** [See Agent Card documentation](agent-card.md)

### JSON-RPC Endpoint

Main endpoint for etymology requests following Telex A2A protocol.

**Endpoint:** `POST /`

**Content-Type:** `application/json`

## JSON-RPC Methods

### `message/send`

Request etymology information for a word.

#### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": 1,
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "philosophy"
        }
      ],
      "kind": "message"
    }
  }
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | string | Yes | Always `"2.0"` |
| `method` | string | Yes | Always `"message/send"` |
| `id` | number/string | Yes | Request identifier for matching responses |
| `params.message.role` | string | Yes | Always `"user"` |
| `params.message.parts` | array | Yes | Array of message parts |
| `params.message.parts[].kind` | string | Yes | Always `"text"` |
| `params.message.parts[].text` | string | Yes | The word to look up |
| `params.message.kind` | string | Yes | Always `"message"` |

#### Success Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "role": "agent",
    "parts": [
      {
        "kind": "text",
        "text": "Philosophy comes from Greek 'philosophia' (φιλοσοφία)..."
      }
    ],
    "kind": "message",
    "messageId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `jsonrpc` | string | Always `"2.0"` |
| `id` | number/string | Matches request ID |
| `result.role` | string | Always `"agent"` |
| `result.parts` | array | Array of response parts |
| `result.parts[].kind` | string | Always `"text"` |
| `result.parts[].text` | string | Etymology information |
| `result.kind` | string | Always `"message"` |
| `result.messageId` | string | Unique UUID for this response |

#### Error Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error: LLM request failed",
    "data": {
      "detail": "API key invalid or rate limit exceeded"
    }
  }
}
```

#### Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON received |
| -32600 | Invalid Request | Missing required fields |
| -32601 | Method not found | Unsupported method name |
| -32602 | Invalid params | Malformed parameters |
| -32603 | Internal error | Server-side error (LLM, etc) |

## Request Examples

### Basic Etymology Lookup

=== "curl"

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

=== "Python"

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
                    "parts": [{"kind": "text", "text": "robot"}],
                    "kind": "message"
                }
            }
        }
    )

    data = response.json()
    etymology = data["result"]["parts"][0]["text"]
    print(etymology)
    ```

=== "JavaScript"

    ```javascript
    const response = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'message/send',
        id: 1,
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'robot' }],
            kind: 'message'
          }
        }
      })
    });

    const data = await response.json();
    const etymology = data.result.parts[0].text;
    console.log(etymology);
    ```

=== "TypeScript"

    ```typescript
    interface EtymologyRequest {
      jsonrpc: '2.0';
      method: 'message/send';
      id: number;
      params: {
        message: {
          role: 'user';
          parts: Array<{ kind: 'text'; text: string }>;
          kind: 'message';
        };
      };
    }

    interface EtymologyResponse {
      jsonrpc: '2.0';
      id: number;
      result: {
        role: 'agent';
        parts: Array<{ kind: 'text'; text: string }>;
        kind: 'message';
        messageId: string;
      };
    }

    async function getEtymology(word: string): Promise<string> {
      const request: EtymologyRequest = {
        jsonrpc: '2.0',
        method: 'message/send',
        id: Date.now(),
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: word }],
            kind: 'message'
          }
        }
      };

      const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      });

      const data: EtymologyResponse = await response.json();
      return data.result.parts[0].text;
    }

    const etymology = await getEtymology('philosophy');
    ```

### Batch Requests

JSON-RPC 2.0 supports batch requests:

```json
[
  {
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
  },
  {
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": 2,
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "philosophy"}],
        "kind": "message"
      }
    }
  }
]
```

**Response:**

```json
[
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": { ... }
  },
  {
    "jsonrpc": "2.0",
    "id": 2,
    "result": { ... }
  }
]
```

## CORS Configuration

By default, CORS is enabled for all origins in development. For production:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

## Monitoring & Logging

Access logs via stdout:

```bash
uv run uvicorn app.main:app --log-level info
```

Available log levels:

- `critical`
- `error`
- `warning`
- `info`
- `debug`
- `trace`

## Next Steps

- Read [Agent Card](agent-card.md) for metadata format
