from datetime import datetime, timezone

import pandas as pd


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


def transform_flight_data(payload: dict) -> pd.DataFrame:
    """Clean and transform raw OpenSky aircraft data."""

    states = payload.get("states") or []
    flight_df = pd.DataFrame(states, columns=COLUMNS)

    if flight_df.empty:
        return flight_df

    flight_df["callsign"] = flight_df["callsign"].str.strip()

    flight_df = flight_df.dropna(
        subset=["latitude", "longitude"]
    ).copy()

    flight_df["time_position"] = pd.to_datetime(
        flight_df["time_position"],
        unit="s",
        utc=True,
        errors="coerce",
    )

    flight_df["last_contact"] = pd.to_datetime(
        flight_df["last_contact"],
        unit="s",
        utc=True,
        errors="coerce",
    )

    flight_df["altitude_feet"] = (
        flight_df["baro_altitude"] * 3.28084
    ).round(2)

    flight_df["speed_mph"] = (
        flight_df["velocity"] * 2.23694
    ).round(2)

    flight_df["flight_status"] = flight_df["on_ground"].map(
        {
            True: "On Ground",
            False: "In Air",
        }
    )

    flight_df["extracted_at_utc"] = datetime.now(timezone.utc)

    return flight_df