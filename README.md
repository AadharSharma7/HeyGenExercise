# HeyGen Exercise

This repository demonstrates a simulated server and a client library for getting the status of a video translation job. The server simulates a long running job that stays in the "pending" state for a configured amount of time - "pendingTime", then switches to either "completed" or "error". The client library gets the status from this server and uses exponential backoff to prevent excessive load on the server by increasing the delay time between each API call.

## Components

- **Server** (`server/server.py`): A Flask based HTTP server that contains a `/status` endpoint.
- **Client** (`client/client.py`): A Python client library that gets the `/status` endpoint with exponential backoff.
- **Tests** (`tests/test_1.py`): An integration test that starts the server and uses the client library.

## Running the test(s)

You can specifiy any value for 'pendingTime'. This is the amount of time in seconds that the server will sending a "pending" status for until it finally sends "complete" or "error" status.

```bash
pendingTime=10 python3 -m pytest -s tests/
```

## Running the Server

You can specifiy any value for 'pendingTime'. This is the amount of time in seconds that the server will sending a "pending" status for until it finally sends "complete" or "error" status.

```bash
pendingTime=10 python3 server/server.py
```

## Running the Client

```bash
python3 client/client.py
```
