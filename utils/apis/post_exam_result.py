import requests
from utils.apis import get_token
from utils.loader import db_msg as db
import warnings
from environs import Env

env = Env()
env.read_env()

SUBMIT_URL = env.str('POST_EXAM_RESULT_URL')


def post_request_with_bearer_token(url, data, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers, verify=False)
    if response.status_code == 401:
        new_token = get_token()  # Call the synchronous version of get_token
        headers["Authorization"] = f"Bearer {new_token}"
        db.add_active_token(new_token)  # Call the synchronous version of add_active_token
        response = requests.post(url, json=data, headers=headers, verify=False)
    return response


def send_exam_result(tgId, ball, examType=True, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    url = SUBMIT_URL
    token_obj = db.get_active_token()
    if token_obj:
        token = token_obj.get('token', None)
    else:
        token = get_token()
        db.add_active_token(token)

    data = {
        "id": tgId,
        "ball": ball
    }

    response = post_request_with_bearer_token(url, data, token)
    return response
