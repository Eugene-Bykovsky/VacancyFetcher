from terminaltables import AsciiTable

from constants import popular_programming_languages
from hh_api_tools import get_hh_vacancy_salary_statictics
from superjob_api_tools import get_superjob_salary_statictics


def print_salary_statistics_table(stats):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
         'Средняя зарплата']
    ]

    for language, stats in stats.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ])

    table = AsciiTable(table_data)
    print(table.table)


def main():
    print('Вакансии c hh.ru программистов по топовым языкам в Москве за '
          'последний месяц.')
    print_salary_statistics_table(get_hh_vacancy_salary_statictics(
        profession='Программист',
        profession_keywords=popular_programming_languages,
        professional_role=96,
        area=1,
        date_from=30))
    print('Вакансии c superjob.ru программистов по топовым языкам в Москве '
          'за последний месяц.')
    print_salary_statistics_table(get_superjob_salary_statictics(
        profession='Программист',
        profession_keywords=popular_programming_languages,
        city=4,
        catalogues=48,
        date_published=30))


if __name__ == '__main__':
    main()
