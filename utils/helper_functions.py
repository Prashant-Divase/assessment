# utils/helper_functions.py
from faker import Faker
import random,json
from config.config import BASE_URL, AUTH_ENDPOINT, USERNAME, PASSWORD
from datetime import datetime, timedelta
from pathlib import Path
from methods.api_methods import ApiMethods

# Initialize Faker instance
fake = Faker()

def check_response(response, expected_status, expected_body):
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
    assert response.json() == expected_body, f"Expected body {expected_body}, got {response.json()}"


def validate_booking_response(response_data):
    """
    Validates that the response contains at least one booking and that each booking has a non-null booking ID.

    :param response_data: List of dictionaries representing bookings.
    :return: True if validation passes, raises AssertionError otherwise.
    """
    # Check if response_data contains at least one booking
    assert len(response_data) > 0, "Response does not contain any bookings."

    # Check each booking entry for a non-null 'bookingid'
    for booking in response_data:
        assert 'bookingid' in booking, f"Booking entry does not contain 'bookingid': {booking}"
        assert booking['bookingid'] is not None, f"Booking ID is null in entry: {booking}"
    return True

def generate_random_booking_data():
    """Generate random booking data with unique values."""

    # Randomly generate names
    firstname = fake.first_name()
    lastname = fake.last_name()

    # Random total price between 50 and 500
    totalprice = random.randint(50, 500)

    # Random check-in and check-out dates (within 1 year range)
    checkin_date = fake.date_this_year(before_today=True, after_today=False)

    # Convert checkin_date (which is datetime.date) to a string in 'YYYY-MM-DD' format
    checkin_str = checkin_date.strftime('%Y-%m-%d')

    # Generate a random checkout date (up to 15 days after checkin)
    checkout_date = (datetime.strptime(checkin_str, "%Y-%m-%d") + timedelta(days=random.randint(1, 15))).strftime(
        "%Y-%m-%d")

    # Random additional needs
    additionalneeds = random.choice(["Breakfast", "Lunch", "Dinner", "Spa", "Shuttle service"])

    # Constructing the booking data
    booking_data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": True,  # Set default to True
        "bookingdates": {
            "checkin": checkin_str,
            "checkout": checkout_date
        },
        "additionalneeds": additionalneeds
    }

    return booking_data


def normalize_data(data):
    """Normalize the data (convert strings 'True'/'False' to booleans)."""
    if isinstance(data, dict):
        # Recursively normalize all the values in the dictionary
        return {key: normalize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursively normalize all elements in the list
        return [normalize_data(item) for item in data]
    elif isinstance(data, str):
        # Convert 'True'/'False' strings to booleans
        if data.lower() == 'true':
            return True
        elif data.lower() == 'false':
            return False
        return data
    return data


def compare_json_ignore_keys(response1, response2, keys_to_ignore):
    """Compare two JSON responses while ignoring specific keys and normalizing data."""

    # Remove the keys to ignore from both JSONs
    response1_filtered = remove_unwanted_keys(response1, keys_to_ignore)
    response2_filtered = remove_unwanted_keys(response2, keys_to_ignore)

    # Normalize the data in both responses
    response1_normalized = normalize_data(response1_filtered)
    response2_normalized = normalize_data(response2_filtered)

    # Perform comparison
    assert response1_normalized == response2_normalized, f"JSONs do not match. \nResponse 1: {response1_normalized} \nResponse 2: {response2_normalized}"

def compare_json_should_not_same(response1, response2, keys_to_ignore=False):
    """Compare two JSON responses while ignoring specific keys and normalizing data."""

    # Remove the keys to ignore from both JSONs
    if keys_to_ignore:
        response1_filtered = remove_unwanted_keys(response1, keys_to_ignore)
        response2_filtered = remove_unwanted_keys(response2, keys_to_ignore)
        # Normalize the data in both responses
        response1_normalized = normalize_data(response1_filtered)
        response2_normalized = normalize_data(response2_filtered)

    # Perform comparison
    assert response1_normalized != response2_normalized, f"JSONs does match. \nResponse 1: {response1_normalized} \nResponse 2: {response2_normalized}"

def remove_unwanted_keys(json_data, keys_to_remove):
    """Remove specified keys from a JSON object."""
    for key in keys_to_remove:
        if key in json_data:
            del json_data[key]
    return json_data


def generate_token():
    payload = json.dumps({
        "username": USERNAME,
        "password": PASSWORD
    })
    # Construct the URL and make the POST request
    url = BASE_URL + '/' + AUTH_ENDPOINT
    config = {
        'base_url': BASE_URL,
        'auth_endpoint': AUTH_ENDPOINT,
        'username': USERNAME,
        'password': PASSWORD
    }
    # Use the API methods to post and retrieve the token
    api_methods = ApiMethods(config=config)  # Assuming this is correctly implemented elsewhere
    token = api_methods.post(url,data=payload)

    return token.text



