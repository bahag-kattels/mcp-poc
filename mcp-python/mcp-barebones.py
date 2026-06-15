import httpx
from fastmcp import FastMCP
import yaml
from pathlib import Path
from config import HEADERS

curr_file_path = Path(__file__).parent

# Load OpenAPI spec from file
with open(curr_file_path / "specs/{API_NAME}.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

servers = openapi_spec.get("servers", [])
if not servers:
    print("Error: No servers defined in the OpenAPI spec.")
    exit(1)

ENV = "{ENV}"
ENV = ENV.lower()
BASE_URL = None

for server in servers:
    if server.get("description").lower().find(ENV) != -1:
        BASE_URL = server.get("url")
        break

if not BASE_URL:
    print(f"Error: No server found for environment '{ENV}'.")
    exit(1)

# Create HTTP client for target API
client = httpx.AsyncClient(base_url=BASE_URL, headers=HEADERS)

# Generate MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name=openapi_spec.get("info", {{}}).get("title", "UNKNOWN:::MCP Server")
)

if __name__ == "__main__":
    mcp.run(transport="http", port={PORT}, host="0.0.0.0")  # or "sse" for HTTP streaming