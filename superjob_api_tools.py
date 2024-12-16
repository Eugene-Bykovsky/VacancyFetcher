import statistics
import time
from itertools import count

from requests import HTTPError

from datetime_tools import get_date_offset_by_days
from requests_tools import get_response
from salary_utils import predict_salary


def fetch_superjob_vacancies(api_key, date_from=None, **kwargs):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        "X-Api-App-Id": api_key
    }
    params = {**kwargs,
              'date_published': get_date_offset_by_days(
                  date_from) if date_from else None}
    for page in count():
        params["page"] = page
        try:
            response = get_response(url, params=params, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP ошибка: {http_err}")
            break
        except ConnectionError as conn_err:
            print(f"Ошибка соединения: {conn_err}. Повтор через 1 секунду.")
            time.sleep(1)
            continue
        except TimeoutError as timeout_err:
            print(f"Ошибка тайм-аута: {timeout_err}. Повтор через 1 секунду.")
            time.sleep(1)
            continue

        try:
            page_payload = response.json()
        except ValueError as json_err:
            print(f"Ошибка парсинга JSON: {json_err}. Пропускаем страницу.")
            continue

        total_vacancies = page_payload.get('total', 0)
        count_per_page = params.get('count', 20)
        total_pages = (
                (total_vacancies + count_per_page - 1) // count_per_page)
        print(f"Обработка страницы {page + 1} из {total_pages}")

        yield page_payload

        if not page_payload.get('more', False):
            break

        time.sleep(1)


def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') != 'rub':
        return None

    predicted_salary = predict_salary(vacancy.get('payment_from'),
                                      vacancy.get('payment_to'))
    if not predicted_salary:
        return None

    return int(predicted_salary) if predicted_salary != 0 else None


def get_superjob_salary_statictics(api_key, profession,
                                   profession_keywords, city,
                                   catalogues, date_published):
    stats = {}

    for keyword in profession_keywords:
        all_pages = list(
            fetch_superjob_vacancies(api_key,
                                     keyword=f'{profession} {keyword}',
                                     city=city,
                                     catalogues=catalogues,
                                     date_published=date_published))

        vacancies_found = all_pages[0].get('total', 0) if all_pages else 0

        salaries = [
            salary for page in all_pages
            for vacancy in page.get('objects', [])
            if (salary := predict_rub_salary_sj(vacancy))
        ]
        average_salary = int(statistics.mean(salaries)) if salaries else 0

        stats[keyword] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": average_salary,
        }

    return stats
