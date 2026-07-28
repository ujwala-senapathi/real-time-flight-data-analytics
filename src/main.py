from extract import fetch_flight_data
from load import save_processed_data
from transform import transform_flight_data


def run_pipeline() -> None:
    """Run the complete flight-data ETL pipeline."""

    print("Starting flight-data ETL pipeline...")

    payload = fetch_flight_data()

    raw_record_count = len(payload.get("states") or [])
    print(f"Raw aircraft records: {raw_record_count}")

    flight_df = transform_flight_data(payload)

    clean_record_count = len(flight_df)
    print(f"Clean aircraft records: {clean_record_count}")

    if flight_df.empty:
        print("No valid flight data was available.")
        return

    api_timestamp = payload.get("time")

    if api_timestamp is None:
        raise ValueError("The API response did not include a timestamp.")

    output_path = save_processed_data(
        flight_df=flight_df,
        api_timestamp=api_timestamp,
    )

    print(f"Processed data saved to: {output_path}")
    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()