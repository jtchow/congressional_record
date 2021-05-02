import boto3
import requests
from datetime import datetime
from secrets import api_key, aws_access_key_id, aws_secret_access_key


def main(api_key):
    request_url = create_url(api_key)
    res = download_zip(request_url)
    # TODO transfer contents to s3
    return res


def create_url(api_key):
    todays_date = datetime.today().strftime('%Y-04-28')
    request_url = f'https://api.govinfo.gov/packages/CREC-{todays_date}/zip?api_key={api_key}'
    return request_url


def download_zip(request_url):
    local_file_name = create_file_name(request_url)
    res = requests.get(request_url, stream=True)
    with open(local_file_name, 'wb') as local_file:
        for chunk in res.iter_content(chunk_size=128):
            local_file.write(chunk)
    return res


def create_file_name(request_url):
    filename = request_url.split('/')[-2]
    filename = filename + '.zip'
    return filename


def transfer_to_s3(data):
    s3 = get_s3_connection()
    # TODO get bucket
    # TODO put data in bucket


def get_s3_connection():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.resource('s3')
    return s3


if __name__ == "__main__":
    blah = main(api_key)
