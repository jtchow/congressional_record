import requests
from datetime import datetime
from secrets import api_key


def main(api_key):
    download_zip(api_key)
    # where do i put the zip? can i even pick
    # process contents of htm folder
    # upload to s3?


def download_zip(api_key):
    request_url = create_url(api_key)
    res = requests.get(request_url)
    return res.json()


def create_url(api_key):
    todays_date = datetime.today().strftime('%Y-%m-%d')
    request_url = f'https://api.govinfo.gov/CREC-{todays_date}/zip?api_key={api_key}'
    return request_url


if __name__ == "__main__":
    blah = download_zip(api_key)
