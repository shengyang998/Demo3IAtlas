"""Fetch and display JSON responses from the 3I/ATLAS live API."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

BASE_URL = "https://www.3iatlaslive.com"


def fetch_json(path: str, params: dict[str, str] | None = None) -> dict:
    """Retrieve JSON content from the 3I/ATLAS live API."""
    url = urllib.parse.urljoin(BASE_URL, path)
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    print("=== /api/news ===")
    news = fetch_json("/api/news")
    print(json.dumps(news, indent=2))

    print("\n=== /api/weekly ===")
    weekly = fetch_json("/api/weekly")
    print(json.dumps(weekly, indent=2))

    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    later = now + timedelta(hours=6)
    params = {
        "start": now.strftime("%Y-%m-%d %H:%M"),
        "stop": later.strftime("%Y-%m-%d %H:%M"),
        "step": "1 hour",
    }

    print("\n=== /api/positions ===")
    positions = fetch_json("/api/positions", params)
    print(json.dumps(positions, indent=2))

    print("\n=== /api/horizons ===")
    horizons_params = params | {"lat": "40", "lon": "-105"}
    horizons = fetch_json("/api/horizons", horizons_params)
    print(json.dumps(horizons, indent=2))


if __name__ == "__main__":
    main()
