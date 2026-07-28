import requests

from config import API_URL


def fetch_flight_data():
    """
    Fetch live aircraft data from the OpenSky API.
    """

    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    return response.json()