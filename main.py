from requests_tools import get_response
from json import dumps


def fetch_hh_vacancies():
    url = 'https://api.hh.ru/vacancies'
    params = {
        'professional_role': 96
    }
    return dumps(get_response(url, params).json(), indent=4)


def main():
    print(fetch_hh_vacancies())


if __name__ == '__main__':
    main()
