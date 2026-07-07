import json
from typing import Any

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.core.config import settings
from app.core.redis import redis_client


SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly",
]


CLIENT_CONFIG = {
    "web": {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}


def _create_flow() -> Flow:
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
    )

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    return flow


def create_authorization(user_id: int) -> str:

    flow = _create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    redis_client.setex(
        f"oauth:{state}",
        settings.GOOGLE_OAUTH_STATE_EXPIRE_SECONDS,
        json.dumps(
            {
                "user_id": user_id,
                "code_verifier": flow.code_verifier,
            }
        ),
    )

    return authorization_url


def exchange_code(
    code: str,
    state: str,
) -> tuple[Credentials, int]:

    cached = redis_client.get(f"oauth:{state}")

    if cached is None:
        raise ValueError("OAuth session expired.")

    cached = json.loads(cached)

    flow = _create_flow()

    flow.code_verifier = cached["code_verifier"]

    flow.fetch_token(code=code)

    redis_client.delete(f"oauth:{state}")

    return (
        flow.credentials,
        cached["user_id"],
    )


def get_user_info(
    credentials: Credentials,
) -> dict[str, Any]:

    service = build(
        "oauth2",
        "v2",
        credentials=credentials,
        cache_discovery=False,
    )

    return service.userinfo().get().execute()
