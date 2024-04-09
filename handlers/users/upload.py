import requests
import os
from icecream import ic
# from data.config import domain_name, origin

domain_name="crmapi.mentalaba.uz"
origin = 'admission.tiiu.uz'

def upload_new_file(token, filename):
    url = f"https://{domain_name}/v1/files/upload"

    headers = {
        'accept': 'application/json', 
        'Authorization': f'Bearer {token}',
        'Origin': f'{origin}',
    }

    # Построение полного пути к файлу
    script_directory_path = os.path.dirname(os.path.abspath(__file__))
    project_directory_path = os.path.abspath(os.path.join(script_directory_path, '..', '..'))
    full_image_path = os.path.join(project_directory_path, filename)

    # ic(full_image_path)


    try:
        file1 = open(full_image_path, 'rb')
        print("Файл успешно открыт:", full_image_path)
        # files = {
        # 'file': (full_image_path, file1, 'image/jpeg'),
        # }
        files = {
                'file': (os.path.basename(full_image_path), file1, 'image/jpeg'),
                 'associated_with': (None, 'users'),
                'usage': (None, 'diploma')
            }
        # data = {
        #     'associated_with': (None, 'users'),
        #     'usage': (None, 'diploma')
        # }

        response = requests.post(url, headers=headers, files=files)
        file1.close()
        # a = response.json()
        # ic(a)
        # print(a['path'])
        return response
    except FileNotFoundError:
        print("Ошибка: файл не найден по пути:", full_image_path)


# filename = 'diploma_files/tg_image_1225547219.jpeg'
# tokens = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzc2LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci81ODliZTEwMS1lZGRiLTQ1MDgtYTQxYi0wOTU2NDkzMzc5ZmUuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMjhUMDk6NTI6MDguMTQyWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTI4VDA5OjUyOjA4LjE0MloiLCJ1bml2ZXJzaXR5SWQiOjEsImlhdCI6MTcxMjUxNzg3OSwiZXhwIjoxNzEyNTM5NDc5fQ.daCinQhZeNSJ7lUs7bJaweK_37VbhjmKCOwDElfEUFg'
# upload_new_file(tokens, filename)


def upload_new_file_sertificate(token, filename):
    url = f"https://{domain_name}/v1/files/upload"

    headers = {
        'accept': 'application/json', 
        'Authorization': f'Bearer {token}',
        'Origin': f'{origin}',
    }

    # Построение полного пути к файлу
    script_directory_path = os.path.dirname(os.path.abspath(__file__))
    project_directory_path = os.path.abspath(os.path.join(script_directory_path, '..', '..'))
    full_image_path = os.path.join(project_directory_path, filename)

    # ic(full_image_path)


    try:
        file1 = open(full_image_path, 'rb')
        print("Файл успешно открыт:", full_image_path)
        # files = {
        # 'file': (full_image_path, file1, 'image/jpeg'),
        # }
        files = {
                'file': (os.path.basename(full_image_path), file1, 'image/jpeg'),
                 'associated_with': (None, 'users'),
                'usage': (None, 'certificate')
            }
        # data = {
        #     'associated_with': (None, 'users'),
        #     'usage': (None, 'diploma')
        # }

        response = requests.post(url, headers=headers, files=files)
        file1.close()
        # a = response.json()
        # ic(a)
        # print(a['path'])
        return response
    except FileNotFoundError:
        print("Ошибка: файл не найден по пути:", full_image_path)