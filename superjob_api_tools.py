import statistics
import time
from itertools import count

from environs import Env
from requests import HTTPError

from datetime_tools import get_date_offset_by_days
from requests_tools import get_response
from salary_utils import predict_salary

env = Env()
env.read_env()

API_KEY_SUPERJOB = env("API_KEY_SUPERJOB")


def fetch_superjob_vacancies(date_from=None, **kwargs):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        "X-Api-App-Id": API_KEY_SUPERJOB
    }
    params = {**kwargs,
              'date_published': get_date_offset_by_days(date_from) if date_from else None}
    for page in count():
        params["page"] = page
        try:
            response = get_response(url, params=params, headers=headers)
            response.raise_for_status()
            page_payload = response.json()

            total_vacancies = page_payload.get('total', 0)
            count_per_page = params.get('count', 20)
            total_pages = ((total_vacancies + count_per_page - 1)
                           // count_per_page)
            print(f"Обработка страницы {page + 1} из {total_pages}")

            yield page_payload
            time.sleep(1)
            if not page_payload.get('more', False):
                break

            time.sleep(1)
        except HTTPError as http_err:
            print(f"HTTP ошибка: {http_err}")
            break
        except Exception as err:
            print(f"Ошибка: {err}")
            break


def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') != 'rub':
        return None

    predicted_salary = int(predict_salary(vacancy.get('payment_from'),
                                          vacancy.get('payment_to')))
    return predicted_salary if predicted_salary != 0 else None


def get_superjob_salary_statictics(profession,
                                   profession_keywords, city,
                                   catalogues, date_published):
    stats = {}

    for keyword in profession_keywords:
        all_pages = list(
            fetch_superjob_vacancies(keyword=f'{profession} {keyword}',
                                     city=city,
                                     catalogues=catalogues,
                                     date_published=date_published))

        vacancies_found = sum(len(page.get('objects', 0)) for page in
                              all_pages)

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
