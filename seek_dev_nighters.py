from datetime import datetime

import pytz

import requests


def load_api_page_data(url, page=1):
    api_response = requests.get(url, params={'page': page})
    api_page_data = api_response.json()
    return api_page_data


def load_attempts(api_url_page):
    pages = load_api_page_data(api_url_page)['number_of_pages']
    for page in range(pages):
        attempts = load_api_page_data(api_url_page, page + 1)['records']
        for attempt in attempts:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }


def get_midnighters(get_attempt, morning=5):
    midnighters = []
    for attempt in get_attempt:
        attempt_timezone = pytz.timezone(attempt['timezone'])
        attempt_time = attempt_timezone.localize(
            datetime.fromtimestamp(attempt['timestamp'])
        )
        if attempt_time.hour < morning:
            midnighters.append(attempt['username'])
    return set(midnighters)


def main():
    api_url_page = 'http://devman.org/api/challenges/solution_attempts/'
    get_attempt = load_attempts(api_url_page)
    midnighters = get_midnighters(get_attempt)
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    main()
