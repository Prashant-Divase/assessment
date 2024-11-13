import pytest,json
import yaml
import requests
from pathlib import Path


def load_config(env):
    """Load environment-specific config from a YAML file."""
    config_path = Path(__file__).parent / "config" / "config.yaml"
    with open(config_path, 'r') as file:
        all_configs = yaml.safe_load(file)

    # Select the config for the specified environment
    config_data = all_configs.get(env)
    if not config_data:
        raise ValueError(f"Configuration for environment '{env}' not found.")

    return config_data

# def generate_token(config):
#     """Generate an authentication token using credentials from config.yaml."""
#     url = f"{config['base_url']}/{config['endpoint']}"
#
#     payload = json.dumps({
#         "username": config['username'],
#         "password": config['password']
#     })
#
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.post(url, headers=headers, data=payload)
#     if response.status_code == 200:
#         token = response.json().get("token")
#         if token:
#             print(f"token is-- {token} ")
#             return token
#         else:
#             raise ValueError("Token not found in the response.")
#     else:
#         raise Exception(f"Failed to obtain token: {response.status_code} {response.text}")

def generate_token(config):
    """Generate an authentication token using credentials from config.yaml."""
    url = f"{config['base_url']}/{config['endpoint']}"

    payload = json.dumps({
        "username": config['username'],
        "password": config['password']
    })

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # This will raise an exception for HTTP error codes (e.g. 4xx, 5xx)

        # Try to extract token from the response
        token = response.json().get("token")
        if token:
            print(f"Token is: {token}")
            return token
        else:
            print("Token not found in the response.")
            return None  # Return None if token is not found, instead of raising an error

    except requests.exceptions.RequestException as e:
        # Handle any request-specific errors, such as connection problems
        print(f"Request failed: {e}")
        return None  # Return None if the request fails

    except Exception as e:
        # Catch other unexpected exceptions
        print(f"An error occurred while generating the token: {e}")
        return None  # Return None if any other error occurs


def pytest_addoption(parser):
    """Add the --env option to specify the environment for tests."""
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests against (qa, staging, etc.)")


@pytest.fixture(scope="session")
def config(request):
    """Load the environment-specific config and generate the token if required."""
    env = request.config.getoption("--env")
    config_data = load_config(env)
    # If the config specifies to use a token, generate it
    if config_data.get("use_token", False):
        token = generate_token(config_data)
        print(f"this called token {token}")
        config_data["token"] = token  # Add token to the config data

    return config_data
