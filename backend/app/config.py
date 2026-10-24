import os
from pathlib import Path

CACHE_DIR = Path(os.getenv("CACHE_DIR", "./data/cache"))
FUELHH_CACHE = CACHE_DIR / "fuelhh.json"
WINDFOR_CACHE = CACHE_DIR / "windfor.json"
ELEXON_BASE = os.getenv("ELEXON_BASE", "https://data.elexon.co.uk/bmrs/api/v1")
OFFLINE = os.getenv("OFFLINE", "0") == "1"
DEFAULT_DECISION_MODE = os.getenv("DECISION_MODE", "gate")  # gate | lead
DEFAULT_GATE_TIME = os.getenv("GATE_TIME", "09:10")
DEFAULT_LEAD_HOURS = float(os.getenv("LEAD_HOURS", "24"))
DEFAULT_TOLERANCE_MIN = int(os.getenv("TOLERANCE_MIN", "60"))
DELIVERY_START = os.getenv("DELIVERY_START", "2026-01-01")
DELIVERY_END = os.getenv("DELIVERY_END", "2026-01-31")
WINDFOR_PUBLISH_FROM = os.getenv("WINDFOR_PUBLISH_FROM", "2025-12-28")
WINDFOR_PUBLISH_TO = os.getenv("WINDFOR_PUBLISH_TO", "2026-02-01")
