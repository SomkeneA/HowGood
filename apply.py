"""Submit an application to HowGood's apply API with an HMAC-SHA256 signed request."""
import hashlib
import hmac
import json
import os
import sys

import requests

ENDPOINT = "https://howgood-apply-api.howgood.workers.dev/apply"
SECRET = "hg2026_python_engineer@!"  # published in HowGood's public how-to docs


def sign(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def build_payload() -> dict:
    payload = {
        "name": "Somkene Anochie",
        "email": "somkeanochie@gmail.com",
        "resume": os.environ["RESUME_URL"],
        "location": "Zionsville, IN, USA",
        "linkedin": "https://www.linkedin.com/in/somkene-anochie",
        "codeLink": os.environ["CODE_LINK"],
        "repos": "https://github.com/SomkeneA",
    }
    for key, env in (("yearsPython", "YEARS_PYTHON"), ("yearsDjango", "YEARS_DJANGO")):
        if os.environ.get(env):
            payload[key] = int(os.environ[env])
    return payload


def main() -> int:
    body = json.dumps(build_payload(), separators=(",", ":")).encode()
    resp = requests.post(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "application/json", "X-HMAC-Signature": sign(body, SECRET)},
        timeout=30,
    )
    print(resp.status_code, resp.text)
    return 0 if resp.status_code == 201 else 1


if __name__ == "__main__":
    sys.exit(main())
