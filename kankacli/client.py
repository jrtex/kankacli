from typing import Any, Iterator
import httpx

BASE_URL = "https://api.kanka.io/1.0"


class KankaError(Exception):
    pass


class KankaClient:
    def __init__(self, token: str):
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def _handle(self, response: httpx.Response) -> Any:
        if response.status_code == 204:
            return None
        if response.status_code == 401:
            raise KankaError("Unauthorized — check your API token.")
        if response.status_code == 404:
            raise KankaError("Not found.")
        if response.status_code == 429:
            raise KankaError("Rate limit exceeded. Wait a moment and retry.")
        if response.status_code == 422:
            detail = response.json().get("errors", response.text)
            raise KankaError(f"Validation error: {detail}")
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: dict | None = None) -> Any:
        return self._handle(self._http.get(path, params=params))

    def post(self, path: str, data: dict) -> Any:
        return self._handle(self._http.post(path, json=data))

    def put(self, path: str, data: dict) -> Any:
        return self._handle(self._http.put(path, json=data))

    def patch(self, path: str, data: dict) -> Any:
        return self._handle(self._http.patch(path, json=data))

    def delete(self, path: str) -> None:
        self._handle(self._http.delete(path))

    def paginate(self, path: str, params: dict | None = None) -> Iterator[dict]:
        """Yield all items across all pages for a list endpoint."""
        params = dict(params or {})
        page = 1
        while True:
            params["page"] = page
            result = self.get(path, params=params)
            yield from result.get("data", [])
            if not result.get("links", {}).get("next"):
                break
            page += 1

    def campaign_url(self, campaign_id: int, *parts: str | int) -> str:
        tail = "/".join(str(p) for p in parts)
        return f"/campaigns/{campaign_id}/{tail}"

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._http.close()
