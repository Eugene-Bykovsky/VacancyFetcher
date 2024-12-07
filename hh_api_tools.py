import statistics
from collections import OrderedDict

from requests_tools import get_response
from datetime_tools import get_date_offset_by_days


def fetch_hh_vacancies(professional_role=None, area=None, date_from=None,
                       text=None):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'professional_role': professional_role,
        'area': area,
        'date_from': get_date_offset_by_days(date_from) if date_from else None,
        'text': text
    }
    return get_response(url, params).json()


def get_vacancy_count_by_text(text):
    return fetch_hh_vacancies(text=text).get('found', 0)


def get_vacancy_count_by_profession_plus_keyword(profession,
                                                 profession_keywords):
    stats = {}
    for keyword in profession_keywords:
        stats[keyword] = get_vacancy_count_by_text(
            text=f'{profession} {keyword}')
    return stats


def get_vacancy_salary_statictics_by_profession_plus_keyword(profession,
                                                             profession_keywords):
    stats = {}

    for keyword in profession_keywords:
        salaries = [predict_rub_salary(python_vacancy_salary)
                    for python_vacancy_salary in get_vacancy_salary_statictics(
                text=f'{profession} {keyword}')
                    if predict_rub_salary(python_vacancy_salary) is not None]
        stats[keyword] = {
            "vacancies_found": get_vacancy_count_by_text(
                text=f'{profession} {keyword}'),
            "vacancies_processed": len(salaries),
            "average_salary": int(
                statistics.mean(salaries)) if salaries else 0,
        }
    return stats


def get_vacancy_salary_statictics(text):
    vacancies = fetch_hh_vacancies(text=text).get('items', 0)
    return [vacancy.get('salary') for vacancy in vacancies]


def predict_rub_salary(salary):
    if salary is None:
        return None
    salary_from = salary.get('from')
    salary_to = salary.get('to')
    if salary['currency'] != 'RUR':
        return None
    if salary_from is None and salary_to is not None:
        return salary_to * 0.8
    elif salary_from is not None and salary_to is None:
        return salary_from * 1.2
    else:
        return (salary_from + salary_to) / 2
