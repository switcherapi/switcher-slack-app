import os

from dotenv import load_dotenv

load_dotenv()

SWITCHER_URL = os.environ.get("SWITCHER_URL")
SWITCHER_API_URL = os.environ.get("SWITCHER_API_URL")
RELEASE_TIME = os.environ.get("RELEASE_TIME", "latest")
VERSION = f"2.0.1 {RELEASE_TIME}"