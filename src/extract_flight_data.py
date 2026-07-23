from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import requests


API_URL = "https://opensky-network.org/api/states/all"

COLUMNS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]


def extract_flight_data() -> tuple[pd.DataFrame, int]:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    payload = response.json()
    states = payload.get("states") or []

    flight_df = pd.DataFrame(states, columns=COLUMNS)
    return flight_df, payload["time"]


def transform_flight_data(flight_df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = flight_df.copy()

    cleaned_df["callsign"] = cleaned_df["callsign"].str.strip()

    cleaned_df = cleaned_df.dropna(
        subset=["longitude", "latitude"]
    )

    cleaned_df["time_position"] = pd.to_datetime(
        cleaned_df["time_position"],
        unit="s",
        utc=True,
        errors="coerce",
    )

    cleaned_df["last_contact"] = pd.to_datetime(
        cleaned_df["last_contact"],
        unit="s",
        utc=True,
        errors="coerce",
    )

    cleaned_df["altitude_feet"] = (
        cleaned_df["baro_altitude"] * 3.28084
    ).round(2)

    cleaned_df["speed_mph"] = (
        cleaned_df["velocity"] * 2.23694
    ).round(2)

    cleaned_df["flight_status"] = cleaned_df["on_ground"].map(
        {
            True: "On Ground",
            False: "In Air",
        }
    )

    cleaned_df["extracted_at_utc"] = datetime.now(timezone.utc)

    return cleaned_df


def save_processed_data(
    cleaned_df: pd.DataFrame,
    api_timestamp: int,
) -> Path:
    output_directory = Path("data/processed")
    output_directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.fromtimestamp(
        api_timestamp,
        tz=timezone.utc,
    ).strftime("%Y%m%d_%H%M%S")

    output_path = (
        output_directory
        / f"flight_data_{timestamp}.csv"
    )

    cleaned_df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    raw_df, api_timestamp = extract_flight_data()
    cleaned_df = transform_flight_data(raw_df)
    output_path = save_processed_data(
        cleaned_df,
        api_timestamp,
    )

    print(f"Raw aircraft records: {len(raw_df)}")
    print(f"Clean aircraft records: {len(cleaned_df)}")
    print(f"Processed data saved to: {output_path}")

    print("\nSelected transformed columns:")
    print(
        cleaned_df[
            [
                "callsign",
                "origin_country",
                "latitude",
                "longitude",
                "altitude_feet",
                "speed_mph",
                "flight_status",
            ]
        ].head()
    )


if __name__ == "__main__":
    main()