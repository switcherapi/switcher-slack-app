# Usage: Set SWITCHER_JWT_SECRET in your environment or .env file
# Example: python tests/generate_token.py resource_id
import os
import jwt
import datetime

from flask.cli import load_dotenv

load_dotenv()

SECRET = os.environ.get("SWITCHER_JWT_SECRET", "changeit")
ALGORITHM = "HS256"
ISSUER = "Switcher Slack App"

import sys
if len(sys.argv) < 2:
    print("Usage: python generate_token.py <resource>")
    sys.exit(1)
resource = sys.argv[1]

payload = {
    "iss": ISSUER,
    "sub": resource,
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=30)
}

token = jwt.encode(payload=payload, key=SECRET, algorithm=ALGORITHM)
print(token)
