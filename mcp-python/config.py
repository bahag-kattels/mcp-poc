import os
import dotenv

dotenv.load_dotenv()
## only supports apis that use API_KEYS for authentication
API_KEY = os.getenv("API_KEY")
HEADERS = {
    "Content-Type": "application/json",
    "apikey": API_KEY,
}