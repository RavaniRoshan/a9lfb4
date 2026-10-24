import json
from pathlib import Path
from typing import Any, List

import httpx

from app.config import (
    ELEXON_BASE,
    FUELHH_CACHE,
    WINDFOR_CACHE,
    OFFLINE,
    DELIVERY_START,
    DELIVERY_END,
    WINDFOR_PUBLISH_FROM,
    WINDFOR_PUBLISH_TO,
)


def _load_cache(path: Path) -> Any:
    if path.exists():
        return json.loads(path.read_text())
    return None


def _save_cache(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def fetch_fuelhh(force: bool = False) -> List[dict]:
    if OFFLINE:
        cached = _load_cache(FUELHH_CACHE)
        if cached is None:
            raise RuntimeError("offline mode but no cache")
        return cached
    if not force:
        cached = _load_cache(FUELHH_CACHE)
        if cached is not None:
            return cached
    url = f"{ELEXON_BASE}/datasets/FUELHH/stream"
    params = {"fuelType": "WIND", "settlementDateFrom": DELIVERY_START, "settlementDateTo": DELIVERY_END}
    try:
        r = httpx.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
    except Exception:
        cached = _load_cache(FUELHH_CACHE)
        if cached is not None:
            return cached
        raise
    _save_cache(FUELHH_CACHE, data)
    return data


def fetch_windfor(force: bool = False) -> List[dict]:
    if OFFLINE:
        cached = _load_cache(WINDFOR_CACHE)
        if cached is None:
            raise RuntimeError("offline mode but no cache")
        return cached
    if not force:
        cached = _load_cache(WINDFOR_CACHE)
        if cached is not None:
            return cached
    url = f"{ELEXON_BASE}/datasets/WINDFOR/stream"
    params = {"publishDateTimeFrom": f"{WINDFOR_PUBLISH_FROM}T00:00:00Z", "publishDateTimeTo": f"{WINDFOR_PUBLISH_TO}T00:00:00Z"}
    try:
        r = httpx.get(url, params=params, timeout=120)
        r.raise_for_status()
        data = r.json()
    except Exception:
        cached = _load_cache(WINDFOR_CACHE)
        if cached is not None:
            return cached
        raise
    _save_cache(WINDFOR_CACHE, data)
    return data
