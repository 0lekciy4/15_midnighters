from datetime import datetime

import pytz

import requests


def load_api_page_data(url, page=1):
    api_response = requests.get(url, params={'page': page})
    api_page_data = api_response.json()
    return api_page_data


def load_attempts(api_url):
    page = 1
    while True:
        page_data = load_api_page_data(api_url, page)
        pages = page_data['number_of_pages']
        attempts = page_data['records']
        for attempt in attempts:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }
        page += 1
        if page > pages:
            break


def get_midnighters(attempts, morning=5):
    midnighters = []
    for attempt in attempts:
        attempt_timezone = pytz.timezone(attempt['timezone'])
        attempt_time = datetime.fromtimestamp(
            attempt['timestamp'],
            attempt_timezone,
        )
        if attempt_time.hour < morning:
            midnighters.append(attempt['username'])
    return set(midnighters)


def main():
    api_url = 'http://devman.org/api/challenges/solution_attempts/'
    attempts = load_attempts(api_url)
    midnighters = get_midnighters(attempts)
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    main()
