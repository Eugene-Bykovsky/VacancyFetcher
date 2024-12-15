import statistics
import time
from itertools import count

from requests import HTTPError

from datetime_tools import get_date_offset_by_days
from requests_tools import get_response
from salary_utils import predict_salary


def fetch_hh_vacancies(date_from=None, **kwargs):
    url = 'https://api.hh.ru/vacancies'
    params = {**kwargs,
              'date_from': get_date_offset_by_days(date_from)
              if date_from else None}
    for page in count():
        params['page'] = page
        try:
            response = get_response(url, params=params)
            page_payload = response.json()
            print(f"Обработка страницы {page} из {page_payload['pages'] - 1}")
            yield page_payload
            if page >= page_payload['pages'] - 1:
                break
            time.sleep(1)
        except HTTPError as http_err:
            if http_err.response.status_code == 502:
                print(
                    f"Ошибка 502 на странице {page}. Пропускаем страницу.")
                time.sleep(1)
                continue
            elif http_err.response.status_code == 403:
                print(f"Доступ запрещен: {http_err}")
            else:
                print(f"HTTP ошибка: {http_err}")
                break
        except Exception as err:
            print(f"Ошибка: {err}")
            break


def get_hh_vacancy_salary_statictics(profession,
                                     profession_keywords,
                                     professional_role,
                                     area, date_from):
    stats = {}

    for keyword in profession_keywords:
        all_pages = list(
            fetch_hh_vacancies(text=f'{profession} {keyword}',
                               professional_role=professional_role,
                               area=area, date_from=date_from))

        vacancies_found = sum(page.get('found', 0) for page in all_pages)
        salaries = [
            salary for page in all_pages
            for vacancy in page.get('items', [])
            if
            (salary := predict_rub_salary_hh(vacancy)) is not None
        ]
        average_salary = int(statistics.mean(salaries)) if salaries else 0

        stats[keyword] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": average_salary,
        }

    return stats


def predict_rub_salary_hh(vacancy):
    if vacancy is None:
        return None
    salary = vacancy.get('salary')
    if salary is None or salary.get('currency') != 'RUR':
        return None

    return int(predict_salary(salary.get('from'), salary.get('to')))
