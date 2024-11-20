import requests


def get_response(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    return response
