from pathlib import Path

API_URL = "https://opensky-network.org/api/states/all"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_FOLDER = PROJECT_ROOT / "data" / "processed"