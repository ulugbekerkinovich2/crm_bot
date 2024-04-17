import requests
from pprint import pprint
import mimetypes
import os
from icecream import ic
import aiofiles
from datetime import datetime
import pytz

# from data.config import  origin, crm_django_domain, username, password
import aiohttp
host = 'crmapi.mentalaba.uz'
origin = 'admission.tiiu.uz'
crm_django_domain = 'alfa.misterdev.uz'
username = 'ulugbek'
password = '998359015a@'

default_header = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'Origin': f'{origin}', 
}

async def check_number(phone):
    url = f'https://{host}/v1/auth/check'
    data = {"phone": phone}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=data) as response:
            if response.status == 201:
                json_data = await response.text()
                return json_data
            else:
                error_message = await response.json()
                return {'error': f'Failed to check number, status_code: {response.status}, details: {error_message}'}

            
# print(check_number('+998998359015').json())


async def user_register(number):
    url = f"https://{host}/v1/auth/register"
    body = {
        "phone": number
    }
    # response = requests.post(url, json=body, headers=default_header)
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=default_header) as response:
            ic(response.status)
            if response.status == 201:
                json_data = await response.json()
                return json_data
            else:
                error_message = await response.json()
                return {'error': f'Failed to user register, status_code: {response.status}, details: {error_message}'}

# user_login('+998998359015')

async def user_verify(secret_code, phone):
    url = f"https://{host}/v1/auth/verify"
    body = {
        'phone': phone,
        "code": secret_code
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=default_header) as response:
            if response.status == 200:
                json_data = await response.json()  # This should be a dictionary
                return {'data': json_data, 'status_code': response.status}  # Return a dictionary
            else:
                return {'error': "Failed to verify", 'status_code': response.status}


    
# user_verify(175654, '+998998359015')

async def user_login(phone):
    url = f"https://{host}/v1/auth/login"
    body = {
        'phone': phone
    }
    # response = requests.post(url, json=body, headers=default_header)
    # print(response.json())
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            if response.status == 200:
                json_data = await response.json() 
                return {'data': json_data, 'status_code': response.status} 
            else:
                return {'error': "Failed to verify", 'status_code': response.status}
            
# user_login('+998998359015')

async def application_form_info(birth_date, document, token):
    url = f'https://{host}/v1/application-forms/info'
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': str(birth_date),
        'document': str(document)
    }
    # response = requests.post(url, json=body, headers=default_header)
    # pprint(response.json())
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            ic(response.status, 'info')
            json_data = await response.json() 
            if response.status == 200:
                
                return {'data': json_data, 'status_code': response.status} 
            else:
                # json_data = await response.json() 
                return {'error': "Failed to verify", 'status_code': response.status, 'data': json_data}
            
# a = application_form_info('2002-04-28', 'AB9666486', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQ5LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci9jNjg5MmQ0OC1mZjQ2LTQ1MjctYmVkMi05MTgzMGJkZDk1ZDcuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTlUMDQ6NDA6NTMuMzkxWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTE5VDA0OjQwOjUzLjM5MVoiLCJ1bml2ZXJzaXR5SWQiOjIsImlhdCI6MTcxMzA4NTcxMiwiZXhwIjoxNzEzMTA3MzEyfQ.lM2EPgio7D9WnDIWZh-HgJa1J0cu6iyk5gNed3x3puM')

# ic(a)

def application_form(token,birth_date,birth_place,citizenship,extra_phone,first_name,gender,last_name,phone,photo,pin,serial_number,src,third_name):
    url = f"https://{host}/v1/application-forms"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': birth_date,
        'birth_place': birth_place,
        'citizenship': citizenship,
        'extra_phone': extra_phone,
        'first_name': first_name,
        'gender': gender,
        'last_name': last_name,
        'phone': phone,
        'photo': photo,
        'pin': pin,
        'serial_number': serial_number,
        'src': src,
        'third_name': third_name
    }
    # print(body)
    response = requests.post(url, headers=default_header, json=body)
    return response


def application_form_manual(token,birth_date,birth_place,email,extra_phone,first_name,gender,last_name,phone,photo,pin,serial_number,src,third_name):
    url = f"https://{host}/v1/application-forms"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': birth_date,
        'birth_place': birth_place,
        'email': email,
        'extra_phone': extra_phone,
        'first_name': first_name,
        'gender': gender,
        'last_name': last_name,
        'phone': phone,
        'photo': photo,
        'pin': pin,
        'serial_number': serial_number,
        'src': src,
        'third_name': third_name
    }
    (162, body)
    response = requests.post(url, headers=default_header, json=body)
    if response.status_code == 201:
        data = response.json()  # Read and parse the JSON response
        return {'data': data, 'status_code': response.status_code}  # Return the data
    else:
        data = response.json() 
        # Handling errors by returning a simple error message or dict
        return {'data': data, 'error': 'Failed to fetch data', 'status_code': response.status_code}
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=default_header, json=body) as response:
    #         if response.status == 201:
    #             data = await response.json()  # Read and parse the JSON response
    #             return data
    #         else:
    #             # Handling errors by returning a simple error message or dict
    #             return {'error': 'Failed to fetch data', 'status_code': response.status}

async def directions(token):
    url = f'https://{host}/v1/directions'
    default_header['Authorization'] = f'Bearer {token}'
    # response = requests.get(url, headers=default_header)
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()  # Read and parse the JSON response
                return data
            else:
                # Handling errors by returning a simple error message or dict
                return {'error': 'Failed to fetch data', 'status_code': response.status}

async def applicants(token, degree_id, direction_id, education_language_id, education_type_id, work_experience_document=None):
    url = f"https://{host}/v1/applicants"
    headers = default_header.copy()
    headers['Authorization'] = f'Bearer {token}'
    body = {
        'degree_id': degree_id,
        'direction_id': direction_id,
        'education_language_id': education_language_id,
        'education_type_id': education_type_id,
        'work_experience_document': work_experience_document
    }
    # ic(body)
    # response = requests.post(url, json=body, headers=default_header)
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            # ic(173, response.status, response.)
            if response.status == 201:
                data = await response.json()  # Read and parse the JSON response
                return data
            else:
                # Handling errors by returning a simple error message or dict
                return {'error': 'Failed to fetch data', 'status_code': response.status}

def update_applicant(token, degree_id, direction_id, education_language_id, education_type_id, applicant_id):
    url = f"https://{host}/v1/applicants/{applicant_id}"  # Assuming you need to specify which applicant to update
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        'degree_id': degree_id,
        'direction_id': direction_id,
        'education_language_id': education_language_id,
        'education_type_id': education_type_id
    }
    response = requests.patch(url, json=body, headers=headers)
    return response.json()
    # async with aiohttp.ClientSession() as session:
    #     async with session.patch(url, json=body, headers=headers) as response:
    #         if response.status == 200:
    #             data = await response
    #             return data
    #         else:
    #             return {'error': 'Failed to update applicant', 'status_code': response.status}

async def my_applications(token):
    url = f"https://{host}/v1/applicants/my-application"
    default_header['Authorization'] = f'Bearer {token}'
    # response = requests.get(url, headers=default_header)
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()  # Read and parse the JSON response
                return data
            else:
                # Handling errors by returning a simple error message or dict
                return {'error': 'Failed to fetch data', 'status_code': response.status}    

def reset_password(phone, token):
    url = f"https://{host}/v1/auth/resend-verify-code"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'phone': phone
    }
    response = requests.post(url, json=body, headers=default_header)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=default_header, json=body) as response:
    #         if response.status == 201:
    #             data = await response.json()  # Read and parse the JSON response
    #             return data
    #         else:
    #             # Handling errors by returning a simple error message or dict
    #             return {'error': 'Failed to fetch data', 'status_code': response.status}

def educations(token):
    url = f"https://{host}/v1/application-forms/educations/"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, headers=default_header) as response:
    #         if response.status == 200:
    #             data = await response.json()  # Read and parse the JSON response
    #             return data
    #         else:
    #             # Handling errors by returning a simple error message or dict
    #             return {'error': 'Failed to fetch data', 'status_code': response.status}

"""
    {
        "id": 1,
        "name_uz": "Maktab",
        "name_ru": "Школа",
        "name_en": "School",
        "created_at": "2024-02-28T15:08:51.352Z",
        "updated_at": "2024-02-28T15:08:51.352Z"
    },
"""

def regions(token):
    url = f"https://{host}/v1/application-forms/regions"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, headers=default_header) as response:
    #         if response.status == 200:
    #             data = await response.json()  # Read and parse the JSON response
    #             return data
    #         else:
    #             # Handling errors by returning a simple error message or dict
    #             return {'error': 'Failed to fetch data', 'status_code': response.status}


def districts(token, district_id):
    url = f"https://{host}/v1/application-forms/districts/{district_id}"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url, headers=default_header) as response:
    #         if response.status == 200:
    #             data = await response.json()  # Asynchronously fetch the data
    #             return data
    #         else:
    #             # It's a good practice to handle HTTP errors
    #             return {'error': 'Failed to fetch data', 'status_code': response.status}


#TODO bu ishlamidi
def upload_file(token, file_name, associated_with, usage): 
    # print('uuuu', file_name)
    url = f"https://{host}/v1/files/upload"
    script_directory_path = os.path.dirname(os.path.abspath(__file__))
    project_directory_path = os.path.abspath(os.path.join(script_directory_path, '..', '..'))
    # ic(project_directory_path)
    full_image_path = os.path.join(project_directory_path,'mukammal-bot-paid', file_name)
    default_header['Authorization'] = f'Bearer {token}'
    # default_header['accept'] = '*/*'
    # # print(local_file_path)
    # ic(full_image_path)
    with open(full_image_path, 'rb') as file:
        # Формирование тела запроса
        files = {
            'file': (full_image_path.split('/')[-1], file, 'image/png'),  # предполагается, что файл - изображение PNG
            'associated_with': (None, associated_with),
            'usage': (None, usage)
        }

    # file1 = open(full_image_path, 'rb')
    # files = {
    #     'file': (full_image_path, file1, 'image/jpeg'),
    #     'associated_with': (None, f'{associated_with}'),
    #     'usage': (None, f'{usage}')
    #     }
        response = requests.post(url, headers=default_header, files=files)
    # file1.close()
    # print(response.json())
    # a = response.json()
    # print(a.get('path', ''))
    # ic(full_image_path)
    return response







    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, data=payload, files=filename) as response:
    #         if response.status == 201:
    #             response_data = await response
    #             return response_data, file_size
    #         else:
    #             return {'error': 'Failed to upload the file.', 'status_code': response.status}            


def application_forms(token,birth_date,birth_place,citizenship,extra_phone,
                      first_name,last_name, gender,phone,photo,pin,serial_number,src,third_name):
    url = f"https://{host}/v1/application-forms"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': birth_date,
        'birth_place': birth_place,
        'citizenhip': citizenship,
        'extra_phone': extra_phone,
        'first_name': first_name,
        'gender': gender,
        'last_name': last_name,
        'phone': phone,
        'photo': photo,
        'pin': pin,
        'serial_number': serial_number,
        'src': src,
        'third_name': third_name
    }
    response = requests.post(url, headers=default_header, json=body)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=default_header, json=body) as response:
    #         if response.status == 201:
    #             data = await response
    #             return data
    #         else:
    #             return {'error': 'Failed to post request', 'status_code': response.status}


async def application_forms_me(token):
    url = f"https://{host}/v1/application-forms/me"
    default_header['Authorization'] = f'Bearer {token}'
    # response = requests.get(url, headers=default_header)

    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to post request', 'status_code': response.status}

async def application_forms_me_new(token):
    url = f"https://{host}/v1/application-forms/me"
    default_header['Authorization'] = f'Bearer {token}'
    # response = requests.get(url, headers=default_header)

    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()
                return {'data': data, 'status_code': response.status} #data
            else:
                return {'error': 'Failed to post request', 'status_code': response.status}


# a =application_forms_me('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQ5LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci9lM2Q0OWJmNi0zNGExLTRhNzktYjZlNS04MWU1OTg3MDRkNWIuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTlUMDQ6NDA6NTMuMzkxWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTE5VDA0OjQwOjUzLjM5MVoiLCJ1bml2ZXJzaXR5SWQiOjIsImlhdCI6MTcxMjA0OTY5OCwiZXhwIjoxNzEyMDcxMjk4fQ.TnhaeCx0OPYgMLwaonkFDWOt_cqZlkzpPieJWN5tL3g')
# pprint(a.json())


async def delete_profile(token):
    url = f"https://{host}/v1/application-forms/delete-profile"
    headers = default_header.copy()
    headers['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 200:
                try:
                    # Attempt to decode JSON regardless of Content-Type header
                    
                    return response.status
                except aiohttp.client_exceptions.ContentTypeError:
                    # Handle the case where JSON decoding fails
                    return {'error': 'Response content type is not application/json', 'status_code': response.status}
            else:
                return {'error': 'Failed to delete profile', 'status_code': response.status}

async def return_token_use_refresh(refreshToken):
    url = f"https://{host}/v1/auth/refresh"
    body = {
        'refreshToken': refreshToken,
    }
    # response = requests.post(url, json=body, headers=default_header)
    # return response
    async with aiohttp.ClientSession() as session:
        async with session.post(url, body=body, headers=default_header) as response:
            if response.status == 201:
                data = await response
                return data
            else:
                return {'error': 'Failed to refresh token', 'status_code': response.status}

def upload_sertificate(token, filename, f_type):
    url = f"https://{host}/v1/certifications/"

    headers = {
        'accept': 'multipart/form-data', 
        'Authorization': f'Bearer {token}',
        'Origin': f'{origin}',
    }
    body = {
        'certification_type': f_type,
        'file': filename
    }
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, data=body) as response:
    #         if response.status == 201:
    #             data = await response.json()
    #             return data
    #         else:
    #             return {'error': 'Failed to upload sertificate', 'status_code': response.status}
    response = requests.post(url, json=body, headers=headers)
    return response.json()
# u_s = upload_sertificate("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQ5LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci9jMjU3MmI1NS02MzA3LTQ3YTEtOGYzNy03NjZjMGFiYTE3ZjIuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTlUMDQ6NDA6NTMuMzkxWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTE5VDA0OjQwOjUzLjM5MVoiLCJ1bml2ZXJzaXR5SWQiOjIsImlhdCI6MTcxMzAyMjI3OCwiZXhwIjoxNzEzMDQzODc4fQ.v5vh5-y6W8jjdVS8jcUpTW1PO5YUBTTRDzWvt9qOxHE",
#                         'certificate/3b2167c7-28d2-4d0b-b69d-87da4d4db3c1.jpg',
#                          'ielts' )
# ic(u_s)


def application_forms_for_edu(token,  district_id, education_id, file_, institution_name, region_id,src='manually'):
    url = f"https://{host}/v1/application-forms"
    default_header['Authorization'] = f"Bearer {token}"
    body = {
        'src': src,
        'user_education': {
            'district_id': district_id,
            'education_id': education_id,
            'file': [file_],
            'institution_name': institution_name,
            'region_id': region_id,
            'src': src
        }
    }
    response = requests.post(url, json=body, headers=default_header)
    return response
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, header=default_header, json=body) as response:
    #         if response.status == 201:
    #             data = await response
    #             return data
    #         else:
    #             return {'error': 'Failed to create application', 'status_code': response.status}

async def djtoken(username, password):
    url = f"https://{crm_django_domain}/api/token/"
    body = {
        'username': username,
        'password': password
    }
    # response = requests.post(url, json=body)
    # return response.json()

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to get token', 'status_code': response.status}

def create_user_profile(token,chat_id,first_name,last_name,pin):
    url = f"https://{crm_django_domain}/create-user-profile/"
    header = {
        'Authorization': f'Bearer {token}'
    } 
    body = {
        'chat_id_user': chat_id,
        'first_name_user': first_name,
        'last_name_user': first_name,
        'pin': pin
    }
    ic(body)
    response = requests.post(url, json=body, headers=header)
    return response.json()

def update_user_profile(id, chat_id, phone, first_name, last_name, pin):
    url = f"https://{crm_django_domain}/user_profile/{chat_id}/update"
    ic(url)
    body = {
        'chat_id_user': chat_id,
        'phone': phone,
        'first_name_user': first_name,
        'last_name_user': last_name,
        'pin': pin
    }
    ic(body)
    response = requests.put(url, json=body)
    return response.json()

# a = update_user_profile(3, "935920479", '998942559015', 'Erkinov', 'Abdulloh', '12341234')
# ic(a)

async def get_all_ser_profile(token):
    url = f"https://{crm_django_domain}/user_profile/"
    header = {
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to fetch data', 'status_code': response.status}

def get_user_profile(chat_id):
    url = f"https://{crm_django_domain}/user_profile/{int(chat_id)}/"
    response = requests.get(url)
    # ic(response.status_code, response.json())
    return response.json()



async def bot_usage(token, start_time, end_time):
    url = f"https://{crm_django_domain}/telegram-bot-usage/"
    header = {
        'Authorization': f'Bearer {token}'
    }
    body = {
        'start_time': start_time,
        'end_time': end_time
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=header) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to fetch data', 'status_code': response.status}


async def download_file(file_url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            print(resp.status)  # Using print for simplicity
            if resp.status == 200:
                # Use aiofiles for async file operations
                async with aiofiles.open(dest, mode='wb') as f:
                    await f.write(await resp.read())


# async def download_file(file_url, dest):
#     os.makedirs(os.path.dirname(dest), exist_ok=True)
    
#     async with aiohttp.ClientSession() as session:
#         async with session.get(file_url) as resp:
#             print(resp.status)  # Using print for simplicity
#             if resp.status == 200:
#                 # Use aiofiles for async file operations
#                 async with aiofiles.open(dest, mode='wb') as f:
#                     await f.write(await resp.read())
                    

def convert_time(iso_datetime_str):
    datetime_obj_utc = datetime.strptime(iso_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    your_timezone = pytz.timezone("Asia/Tashkent")
    datetime_obj_local = datetime_obj_utc.replace(tzinfo=pytz.utc).astimezone(your_timezone)
    # print(datetime_obj_local.strftime("%Y-%m-%d %H:%M:%S %Z"))

# If you just need the date part in your local timezone
    return datetime_obj_local.strftime("%Y-%m-%d")

# iso_datetime_str = "2002-04-27T19:00:00.000Z"
# a =  convert_time(iso_datetime_str)
# ic(a)



                # get_current_user = send_req.get_user_profile(chat_id=message.chat.id)
                # chat_id_user = get_current_user['chat_id_user']
                # id_user = get_current_user['id']
                # await state.update_data(chat_id_user=chat_id_user, id_user=id_user)

                # update_user_data = send_req.update_user_profile(id=id_user, chat_id=chat_id_user, phone=phone_num, first_name="None", last_name="None", pin="None")