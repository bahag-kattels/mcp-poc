import os
from pathlib import Path
import dotenv

dotenv.load_dotenv()
## only supports apis that use API_KEYS for authentication
API_KEY = os.getenv("API_KEY")
SWAGGERHUB_API_KEY = os.getenv("SWAGGERHUB_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "apikey": API_KEY,
}

PARENT = Path(__file__).parent
CONFIG_FOLDER = PARENT / "specs"

if not CONFIG_FOLDER.exists():
    CONFIG_FOLDER.mkdir(parents=True)


SWAGGERHUB_OWNER = "BAHAG"
SWAGGERHUB_HEADERS = {"Accept": "application/yaml", "Authorization": SWAGGERHUB_API_KEY}