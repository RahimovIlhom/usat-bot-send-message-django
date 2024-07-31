import requests
import warnings
from environs import Env

env = Env()
env.read_env()

CREATE_TOKEN_URL = env.str("CREATE_TOKEN_URL")
ADMISSION_USERNAME = env.str('ADMISSION_USERNAME')
ADMISSION_PASSWORD = env.str('ADMISSION_PASSWORD')


def get_token():
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    user_login = {
        "username": ADMISSION_USERNAME,
        "password": ADMISSION_PASSWORD
    }

    response = requests.post(CREATE_TOKEN_URL, json=user_login, verify=False)
    response.raise_for_status()  # This will raise an exception for HTTP error codes
    resp_json = response.json()
    return resp_json['token']
