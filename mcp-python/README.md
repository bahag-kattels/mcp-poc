# mcp-python

Utilities for generating FastMCP servers from OpenAPI specs pulled from SwaggerHub.

## What this project does

The main entry point is `gen-servers.py`. It:

1. Fetches an OpenAPI document from SwaggerHub.
2. Saves the spec into `specs/<api-name>.yaml`.
3. Generates an MCP server script named `mcp-<api-name>-server.py`.
4. Optionally writes a VS Code MCP configuration into `.vscode/mcp.json`.

The generated server reads the saved spec, picks the server URL whose description matches the target environment, and exposes the API through FastMCP.

## Requirements

- Python 3.13 or newer.
- `uv` for running the scripts.
- The SwaggerHub CLI available on your `PATH`.
- An `API_KEY` environment variable for authenticated requests made by the generated server.

## Install

From this folder:

```bash
uv sync
```

If you prefer not to install the project globally, you can still run the scripts with `uv run`.

## Generate a server

Use `gen-servers.py` to create a new server from an API definition:

```bash
uv run gen-servers.py -a api-product-recommendation -v 5.0.0 -p 4000 -e QS -m true
```

Flags:

- `-a, --api-name`: SwaggerHub API name, required.
- `-v, --version`: API version to fetch, defaults to `1.0.0`.
- `-p, --port`: Port used by the generated MCP server, defaults to `4000`.
- `-e, --env`: Environment selector matched against the OpenAPI server description, defaults to `QA`.
- `-m, --mcp-json`: When `true`, also update `.vscode/mcp.json`.

After generation you should see:

- `specs/<api-name>.yaml`
- `mcp-<api-name>-server.py`
- `.vscode/mcp.json` if you enabled the `-m` flag

## Run a generated server

Once a server file has been generated, run it with `uv`:

```bash
API_KEY=your-api-key uv run mcp-api-product-recommendation-server.py
```

The server listens on `0.0.0.0` at the port set during generation.

## Project layout

- `gen-servers.py`: generator for specs, server scripts, and optional VS Code config.
- `mcp-barebones.py`: template copied into generated server files.
- `config.py`: shared configuration, including the SwaggerHub owner and headers.
- `specs/`: saved OpenAPI documents.

## Notes

- The generated server expects the OpenAPI document to include at least one `servers` entry.
- The environment value is matched case-insensitively against each server description.
- If no matching server is found, generation succeeds but the runtime server exits with an error.