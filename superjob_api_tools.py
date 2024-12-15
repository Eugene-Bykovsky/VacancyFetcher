from requests import HTTPError
from environs import Env

from requests_tools import get_response
from salary_utils import predict_salary

env = Env()
env.read_env()

API_KEY_SUPERJOB = env("API_KEY_SUPERJOB")


def fetch_superjob_vacancies(**kwargs):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {**kwargs}
    headers = {
        "X-Api-App-Id": API_KEY_SUPERJOB
    }

    try:
        data = get_response(url, params=params, headers=headers).json()
        vacancies_data = data.get('objects', [])

        vacancies = [
            f"{vacancy.get('profession', 'Не указана')}, "
            f"{vacancy.get('town', {}).get('title', 'Город не указан')}, "
            f"{predict_rub_salary_sj(vacancy)}"
            for vacancy in vacancies_data
            if 'catalogues' in vacancy and vacancy['catalogues'] and
               vacancy['catalogues'][0].get('id') == 33
        ]

        return vacancies
    except HTTPError as http_err:
        if http_err.response.status_code == 502:
            print(f"Ошибка 502: {http_err}")
        elif http_err.response.status_code == 403:
            print(f"Доступ запрещен: {http_err}")
        else:
            print(f"HTTP ошибка: {http_err}")
    except Exception as err:
        print(f"Ошибка: {err}")


def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') != 'rub':
        return None

    predicted_salary = int(predict_salary(vacancy.get('payment_from'),
                                          vacancy.get('payment_to')))
    return predicted_salary if predicted_salary != 0 else None
