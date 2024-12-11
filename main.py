from pprint import pprint

from hh_api_tools import get_hh_vacancy_salary_statictics
from constants import popular_programming_languages
from superjob_api_tools import fetch_superjob_vacancies


def main():
    # pprint(get_hh_vacancy_salary_statictics(
    #     profession='Программист',
    #     profession_keywords=popular_programming_languages))
    pprint(fetch_superjob_vacancies())


if __name__ == '__main__':
    main()
