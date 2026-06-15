import argparse
from pathlib import Path
import yaml
import subprocess
import sys
import json
from config import CONFIG_FOLDER, SWAGGERHUB_OWNER, PARENT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MCP Server Generation Script: Generates a server based on the provided configuration file.")
    parser.add_argument("-a", "--api-name", type=str, help="Name of the API to generate the server for.", required=True)
    parser.add_argument("-v", "--version", type=str, default="1.0.0", help="Version of the API to generate the server for.")
    parser.add_argument("-p", "--port", type=int, default=4000, help="Port number for the generated MCP server.")
    parser.add_argument("-e", "--env", type=str, default="QA", help="Environment to target (e.g., DEV, QA, PROD).")
    parser.add_argument("-m", '--mcp-json', type=bool, default=False, help="Save the server config to .vscode/mcp.json")
    return parser.parse_args()


def save_spec_file(api_name, version) -> None:
    if not version:
        result = subprocess.run(["swaggerhub", "api:get", f"{SWAGGERHUB_OWNER}/{api_name}"], capture_output=True, text=True)
    else:
        result = subprocess.run(["swaggerhub", "api:get", f"{SWAGGERHUB_OWNER}/{api_name}/{version}"], capture_output=True, text=True)

    config_text = result.stdout

    if yaml.safe_load(config_text) is None or result.returncode != 0:
        print(f"Error: API spec for {api_name} is empty or invalid.")
        sys.exit(1)
    
    config_path = CONFIG_FOLDER / f"{api_name}.yaml"
    with open(config_path, "w") as f:
        f.write(config_text)
    print(f"API spec for {api_name} saved to {config_path}")

def generate_server(api_name, env, port, mcp_json) -> None:
    with open("mcp-barebones.py", "r") as f:
        template = f.read()
    
    template = template.format(API_NAME=api_name, ENV=env, PORT=port)

    with open(f"mcp-{api_name}-server.py", "w") as f:
        f.write(template)
    
    if mcp_json:
        mcp_config_path = PARENT.parent / ".vscode" / "mcp.json"

        if not mcp_config_path.parent.exists():
            mcp_config_path.parent.mkdir(parents=True)

        with open(mcp_config_path, "r") as f:
            mcp_config = json.load(f)
            if mcp_config.get("servers") is None:
                mcp_config["servers"] = {}
        
        if api_name in mcp_config['servers']:
            print(f"Warning: Overwriting existing config for {api_name} in {mcp_config_path}")
        mcp_config['servers'][api_name] = {
            "type": "http",
            "url": f"http://localhost:{port}/mcp"
        }
        with open(mcp_config_path, "w") as f:
            json.dump(mcp_config, f, indent=4)
        print(f"Saved MCP server config to {mcp_config_path}")

    print(f"Generated MCP server script: mcp-{api_name}-server.py")


def main():
    args = parse_args()
    print(f"Generating server for API: {args.api_name}")
    save_spec_file(args.api_name, args.version)
    generate_server(args.api_name, args.env, args.port, args.mcp_json)

if __name__ == "__main__":
    main()