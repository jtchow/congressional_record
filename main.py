import boto3
import requests
import zipfile
from datetime import datetime
from secrets import api_key, aws_access_key_id, aws_secret_access_key, bucket_name


def main(api_key):
    request_url = create_url(api_key)
    download_file_name = create_file_name(request_url)
    download_zip(request_url, download_file_name)
    unzip_download(download_file_name)
    # transfer_to_s3(download_file_name)
    # todo delete local file
    return


def create_url(api_key):
    todays_date = datetime.today().strftime('%Y-04-28')
    request_url = f'https://api.govinfo.gov/packages/CREC-{todays_date}/zip?api_key={api_key}'
    return request_url


def create_file_name(request_url):
    filename = request_url.split('/')[-2]
    filename = filename + '.zip'
    return filename


def download_zip(request_url, download_file_name):
    res = requests.get(request_url, stream=True)
    # TODO some kind of error handling
    with open(download_file_name, 'wb') as local_file:
        for chunk in res.iter_content(chunk_size=128):
            local_file.write(chunk)
    return res


def unzip_download(download_file_name):
    with zipfile.ZipFile(download_file_name, 'r') as zipped:
        zipped.extractall('.')


def transfer_to_s3(filename):
    # TODO error handling
    s3 = get_s3_connection()
    s3.Bucket(bucket_name).upload_file(filename, filename)


def get_s3_connection():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.resource('s3')
    return s3


if __name__ == "__main__":
    blah = main(api_key)
