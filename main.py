from pprint import pprint

from hh_api_tools import (fetch_hh_vacancies,
                          get_vacancy_count_by_text,
                          get_vacancy_count_by_profession_plus_keyword,
                          get_vacancy_salary_statictics, predict_rub_salary,
                          get_vacancy_salary_statictics_by_profession_plus_keyword)
from constants import popular_programming_languages


def main():
    # print(fetch_hh_vacancies(professional_role=96, area=1, date_from=30))
    # print(fetch_hh_vacancies(professional_role=96, area=1))
    # print(get_vacancy_count_by_text(text='Программист Python'))
    # pprint(get_vacancy_count_by_profession_plus_keyword(
    #     profession='Программист',
    #     profession_keywords=popular_programming_languages))
    # pprint(get_vacancy_salary_statictics(text='Python'))
    # vacancy = fetch_hh_vacancies(text='Python разработчик')['items'][1]
    # print(vacancy)
    # python_vacancies_salary = get_vacancy_salary_statictics(
    #     text='Программист Python')
    # for python_vacancy_salary in python_vacancies_salary:
    #     pprint(predict_rub_salary(python_vacancy_salary))
    pprint(get_vacancy_salary_statictics_by_profession_plus_keyword(
        profession='Программист',
        profession_keywords=popular_programming_languages))


if __name__ == '__main__':
    main()
