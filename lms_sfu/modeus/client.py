import requests

from lms_sfu import config


class ModeusClient:
    def __init__(self, token: str | None = None, base_url: str | None = None):
        self.token = token or config.TOKEN
        self.base_url = (base_url or config.MODEUS_BASE_URL).rstrip("/")
        if not self.token:
            raise ValueError("TOKEN is not set")

    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:155.0) "
                "Gecko/20100101 Firefox/155.0"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Origin": config.MODEUS_ORIGIN,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "Priority": "u=0",
        }

    def post(self, path: str, json: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        response = requests.post(url, headers=self.headers(), json=json)
        if response.status_code != 200:
            raise RuntimeError(
                f"Modeus request failed ({response.status_code}): {path}"
            )
        return response.json()
