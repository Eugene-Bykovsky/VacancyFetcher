from requests import HTTPError

from requests_tools import get_response
from salary_utils import predict_salary


def fetch_superjob_vacancies(**kwargs):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    params = {**kwargs}
    headers = {
        "X-Api-App-Id": "v3.r.138766998"
                        ".691d125ea8a181380274846268a33cd9267977a8"
                        ".78ea7c7e3d9be6b0d8ef22ebf4ed9526126c13fd "
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
