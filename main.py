import os
import boto3
import requests
import logging
import shutil
import zipfile
from datetime import datetime
from secrets import api_key, aws_access_key_id, aws_secret_access_key, bucket_name


def main(api_key, logger):
    request_url = create_url(api_key, logger)
    folder_name = get_folder_name(request_url)
    download_zip(request_url, folder_name)
    unzip_download(folder_name)
    convert_html_to_txt(folder_name)
    transfer_to_s3(folder_name, logger)
    delete_local_files(folder_name)
    return


def create_url(api_key, logger):
    todays_date = datetime.today().strftime('%Y-%m-%d')
    request_url = f'https://api.govinfo.gov/packages/CREC-{todays_date}/zip?api_key={api_key}'
    logger.info(f'trying to hit {request_url}')
    return request_url


def get_folder_name(request_url):
    filename = request_url.split('/')[-2]
    return filename


def download_zip(request_url, download_file_name, logger):
    res = requests.get(request_url, stream=True)
    if res.ok:
        zip_file_name = download_file_name + '.zip'
        with open(zip_file_name, 'wb') as local_file:
            for chunk in res.iter_content(chunk_size=128):
                local_file.write(chunk)
        logger.info(f'Successfully downloaded file at {request_url}')
    else:
        logger.info(f'Could not access resource at {request_url}')
    return res


def unzip_download(download_file_name):
    zip_file_name = download_file_name + '.zip'
    with zipfile.ZipFile(zip_file_name, 'r') as zipped:
        zipped.extractall('.')


def convert_html_to_txt(folder_name):
    html_folder_path = os.path.join(folder_name, 'html')
    txt_file_path = os.path.join(folder_name, 'txt')
    try:
        os.mkdir(txt_file_path)
        for file in os.listdir(html_folder_path):
            original_file_path = os.path.join(html_folder_path, file)
            new_file_path = os.path.join(txt_file_path, file.split('.')[0] + '.txt')
            os.rename(original_file_path, new_file_path)
    except FileExistsError:
            pass


def transfer_to_s3(parent_folder, logger):
    # TODO error handling
    # todo go into parentfolder/html and for each file in there, upload to s3 with the prefix of parent folder
    s3 = get_s3_connection()
    logger.info('created s3 connection')
    txt_file_path = os.path.join(parent_folder, 'txt')
    for filename in os.listdir(txt_file_path):
        file_path = os.path.join(txt_file_path, filename)
        try:
            s3.Bucket(bucket_name).upload_file(file_path, f'{parent_folder}/{filename}')
        except:
            logger.info(f'could not upload file: {filename}')


def get_s3_connection():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.resource('s3')
    return s3


def delete_local_files(folder_name):
    try:
        shutil.rmtree(folder_name)
        os.remove(f'{folder_name}.zip')
    except FileNotFoundError:
        print(f"Couldn't delete {folder_name}")
        pass


if __name__ == "__main__":
    logger = logging.getLogger('transfer_to_s3_task')
    blah = main(api_key, logger)
