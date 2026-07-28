from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_FOLDER


def save_processed_data(
    flight_df: pd.DataFrame,
    api_timestamp: int,
) -> Path:
    """Save transformed flight data as a timestamped CSV file."""

    PROCESSED_DATA_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.fromtimestamp(
        api_timestamp,
        tz=timezone.utc,
    ).strftime("%Y%m%d_%H%M%S")

    output_path = (
        PROCESSED_DATA_FOLDER
        / f"flight_data_{timestamp}.csv"
    )

    flight_df.to_csv(
        output_path,
        index=False,
    )

    return output_path