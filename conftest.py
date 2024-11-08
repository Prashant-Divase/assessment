import pytest
import yaml
import requests
from pathlib import Path


def load_config(env):
    """Load environment-specific config from a YAML file."""
    config_path = Path(__file__).parent / "config" / f"{env}.yaml"
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def generate_token():
    """Generate an authentication token using credentials from config.yaml."""
    config = load_config()
    url = config['api']['base_url'] + config['api']['auth_endpoint']
    payload = {
        "username": config['api']['username'],
        "password": config['api']['password']
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # Send a POST request to get the token
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        token = response.json().get("token")
        if token:
            return token
        else:
            raise ValueError("Token not found in the response.")
    else:
        raise Exception(f"Failed to obtain token: {response.status_code} {response.text}")

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
        config_data["token"] = token  # Add token to the config data

    return config_data
