# Webhook Logger

A lightweight webhook logging service with HTTP APIs and simple HTML UI.

## Features
- Receive webhooks via POST /webhook
- List recent webhooks via GET /logs
- Get specific webhook via GET /logs/<id>
- Simple HTML UI at GET /
- SQLite storage, no external deps

## Requirements
- Docker or Python 3.12+

## Run (Docker)
```bash
docker-compose up -d
```

## Run (Local)
```bash
pip install -r requirements.txt
python -m flask run --host=0.0.0.0 --port=5000
```

## API Endpoints

### POST /webhook
Receive and store a webhook payload.

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "test", "data": "hello"}'
```

### GET /logs
List recent webhooks (last 50).

```bash
curl http://localhost:5000/logs
```

### GET /logs/<id>
Get specific webhook details.

```bash
curl http://localhost:5000/logs/1
```

## UI
Visit http://localhost:5000/ to see recent webhooks in a table.

## Example Usage

### Test the Webhook Logger
```bash
# Start the service
docker-compose up -d

# Send a test webhook
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "push", "repo": "my-repo", "branch": "main"}'

# Check the logs
curl http://localhost:5000/logs

# View in browser
open http://localhost:5000
```
