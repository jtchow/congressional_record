import os
import boto3
import requests
import zipfile
from datetime import datetime
from secrets import api_key, aws_access_key_id, aws_secret_access_key, bucket_name


def main(api_key):
    request_url = create_url(api_key)
    folder_name = get_folder_name(request_url)
    download_zip(request_url, folder_name)
    unzip_download(folder_name)
    convert_html_to_txt(folder_name)
    transfer_to_s3(folder_name)
    # todo delete local files
    return


def create_url(api_key):
    todays_date = datetime.today().strftime('%Y-04-30')
    request_url = f'https://api.govinfo.gov/packages/CREC-{todays_date}/zip?api_key={api_key}'
    return request_url


def get_folder_name(request_url):
    filename = request_url.split('/')[-2]
    return filename


def download_zip(request_url, download_file_name):
    res = requests.get(request_url, stream=True)
    # TODO some kind of error handling
    zip_file_name = download_file_name + '.zip'
    with open(zip_file_name, 'wb') as local_file:
        for chunk in res.iter_content(chunk_size=128):
            local_file.write(chunk)
    return res


def unzip_download(download_file_name):
    zip_file_name = download_file_name + '.zip'
    with zipfile.ZipFile(zip_file_name, 'r') as zipped:
        zipped.extractall('.')


def convert_html_to_txt(folder_name):
    html_folder_path = os.path.join(folder_name, 'html')
    txt_file_path = os.path.join(folder_name, 'txt')
    os.mkdir(txt_file_path)
    for file in os.listdir(html_folder_path):
        try:
            original_file_path = os.path.join(html_folder_path, file)
            new_file_path = os.path.join(txt_file_path, file.split('.')[0] + '.txt')
            os.rename(original_file_path, new_file_path)
        except FileExistsError:
            continue


def transfer_to_s3(parent_folder):
    # TODO error handling
    # todo go into parentfolder/html and for each file in there, upload to s3 with the prefix of parent folder
    s3 = get_s3_connection()
    txt_file_path = os.path.join(parent_folder, 'txt')
    for filename in os.listdir(txt_file_path):
        file_path = os.path.join(txt_file_path, filename)
        print(f'Uploading {filename}')
        s3.Bucket(bucket_name).upload_file(file_path, f'{parent_folder}/{filename}')


def get_s3_connection():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.resource('s3')
    return s3


if __name__ == "__main__":
    blah = main(api_key)
