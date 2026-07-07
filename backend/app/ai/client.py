import json

import httpx

from app.core.config import settings


class AIClient:

    def __init__(self):

        self.base_url = settings.AI_BASE_URL.rstrip("/")
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0,
    ) -> dict:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": temperature,
        }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    def extract_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:

        response = self.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0,
        )

        content = (
            response["choices"][0]["message"]["content"]
        )

        try:
            return json.loads(content)
        except Exception:
            raise ValueError(
                f"AI returned invalid JSON:\n\n{content}"
            )
