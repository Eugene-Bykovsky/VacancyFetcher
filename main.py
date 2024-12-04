from json import dumps

from requests_tools import get_response
from datetime_tools import get_date_offset_by_days


def fetch_hh_vacancies(professional_role, area, date_from=None):

    url = 'https://api.hh.ru/vacancies'
    params = {
        'professional_role': professional_role,
        'area': area,
        'date_from': get_date_offset_by_days(date_from)
    }
    return dumps(get_response(url, params).json(), indent=4)


def main():
    print(fetch_hh_vacancies(professional_role=96, area=1, date_from=30))
    print(fetch_hh_vacancies(professional_role=96, area=1))


if __name__ == '__main__':
    main()
