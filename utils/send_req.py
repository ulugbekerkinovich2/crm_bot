import requests
from pprint import pprint
import mimetypes
import os
from icecream import ic
import aiofiles
from datetime import datetime
import pytz
import random
from data.config import  origin, crm_django_domain, username, password, origin_grant
from data.config import domain_name as host
from utils.logs import log_to_json
import aiohttp

import requests
from icecream import ic
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# from utils.send_req import default_header
ic(origin, 'oldin')
# =======
ic(origin, 'shu')
# origin = 'admission.uess.uz'
# origin = 'admission.tiiu.uz'
# ic(origin, 'keyingi')
host = 'crmapi.mentalaba.uz'
origin = 'qabul.aifu.uz'
# username = 'ulugbek'
crm_django_domain = 'global.misterdev.uz'
# password = '998359015a@'
# ic.disable()
default_header = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'Origin': f'{origin}', 
}
ic(origin)

async def check_number(phone, is_grant_origin=False):
    url = f'https://{host}/v1/auth/check'
    data = {"phone": phone}
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=data) as response:
            if response.status == 201:
                json_data = await response.text()
                return json_data
            else:
                error_message = await response.json()
                return {'error': f'Failed to check number, status_code: {response.status}, details: {error_message}'}


            
# print(check_number('+998998359015').json())


async def user_register(number, is_grant_origin=False):
    url = f"https://{host}/v1/auth/register"
    body = {
        "phone": number
    }
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=default_header) as response:
            if response.status == 201:
                json_data = await response.json()
                return json_data
            else:
                error_message = await response.json()
                return {'error': f'Failed to user register, status_code: {response.status}, details: {error_message}'}



async def user_verify(secret_code, phone, is_grant_origin=False):
    url = f"https://{host}/v1/auth/verify"
    body = {
        'phone': phone,
        "code": secret_code
    }

    if is_grant_origin:
        default_header['Origin'] = origin_grant
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=default_header) as response:
            data = await response.json()
            if response.status == 200:
                json_data = await response.json()  # This should be a dictionary
                return {'data': json_data, 'status_code': response.status}  # Return a dictionary
            else:
                return {'error': "Failed to verify", 'status_code': response.status}


    


async def user_login(phone, is_grant_origin=False):
    url = f"https://{host}/v1/auth/login"
    body = {
        'phone': phone
    }
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            if response.status == 200:
                json_data = await response.json() 
                return {'data': json_data, 'status_code': response.status} 
            else:
                return {'error': "Failed to verify", 'status_code': response.status}
            

async def application_form_info(birth_date, document, token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f'https://{host}/v1/application-forms/info'
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': str(birth_date),
        'document': str(document),
        'type': 'all'
    }
    ic(104, 'keldi')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            ic(body)
            ic(response.status, 'info')
            ic(111, response)
            if response.status == 200:
                json_data = await response.json() 
                return {'data': json_data , 'status_code': response.status} 
            else:
                error_data = await response.json()
                return {'error': "Failed to verify", 'status_code': response.status, 'data': error_data}

def application_form(token,birth_date,birth_place,citizenship,extra_phone,first_name,gender,last_name,phone,photo,pin,serial_number,src,third_name,
                      is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    try:
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
        response = requests.post(url, headers=default_header, json=body)
        return response
    except:
        response = requests.post(url, headers=default_header, json=body)
        return response


def application_form_manual(token,birth_date,birth_place,email,extra_phone,first_name,gender,last_name,phone,photo,pin,serial_number,src,third_name,
                            is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
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
        log_data = {
            'time': datetime.utcnow().isoformat(),
            'event': 'application_form_manual',
            'details': {
                'body': body
            }
        }
        log_to_json(log_data)
        data = response.json()
        return {'data': data, 'status_code': response.status_code}
    else:
        data = response.json() 
        return {'data': data, 'error': 'Failed to fetch data', 'status_code': response.status_code}

async def directions(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f'https://{host}/v1/directions'
    default_header['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to fetch data', 'status_code': response.status}

async def applicants(token,is_transfer_student,chat_id_user, degree_id, direction_id, education_language_id, education_type_id, work_experience_document=None,
                     is_second_specialty=False, branch=None,is_master=None, referral_source='telegram', is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/applicants"
    headers = default_header.copy()
    headers['Authorization'] = f'Bearer {token}'
    body = {
        'branch': branch,
        'degree_id': int(degree_id),
        'direction_id': int(direction_id),
        'education_language_id': int(education_language_id),
        'education_type_id': int(education_type_id),
        # 'work_experience_document': str(work_experience_document),
        'bot_user_id': str(chat_id_user),
        'is_master': is_master,
        'is_second_specialty': is_second_specialty,
        'is_transfer_student': is_transfer_student,
        'referral_source': referral_source
    }
    ic(body, headers)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            # ic(173, response.status, response.text)
            if response.status == 201:
                return response.status
            else:
                return {'error': response.text, 'status_code': response.status}


def grant_applicant(
    token: str,
    degree_id: int,
    direction_id: int,
    education_language_id: int,
    education_type_id: int,
    is_grant: bool = True
) -> dict:
    url = "https://crmapi.mentalaba.uz/v1/applicants"
    headers = {
        "Authorization": f"Bearer {token}",
        "Origin": origin_grant,
        "Content-Type": "application/json"
    }

    payload = {
        "degree_id": degree_id,
        "direction_id": int(direction_id),
        "education_language_id": int(education_language_id),
        "education_type_id": int(education_type_id),
        "is_grant": is_grant
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            return response.json()
        ic(response.text)
        # Agar xato bo‘lsa
        return {
            "error": f"API {response.status_code} qaytardi",
            "details": response.text
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": "Tarmoq xatosi yoki API ulanmayapti",
            "details": str(e)
        }


def update_applicant(token, degree_id, direction_id, education_language_id, education_type_id, applicant_id):
    try:
        url = f"https://{host}/v1/applicants/{applicant_id}"
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
    except:
        return {'error': 'Failed to fetch data', 'status_code': response.status}

async def my_applications(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/applicants/my-application"
    default_header['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    data = await response.json()
                else:
                    data = await response.text()
                return data
            else:
                return {'error': 'Failed to fetch data', 'status_code': response.status, 'details': await response.text()}
 

def reset_password(phone, token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    try:
        url = f"https://{host}/v1/auth/resend-verify-code"
        default_header['Authorization'] = f'Bearer {token}'
        body = {
            'phone': phone
        }
        response = requests.post(url, json=body, headers=default_header)
        # log_data = {
        #     'time': datetime.utcnow().isoformat(),
        #     'event': 'reset_password',
        #     'details': {
        #         'body': body,
        #         'status_code': response.status,
        #         'data': response.json()
        #     }
        # }
        # log_to_json(log_data)
        return response
    except:
        # log_data = {
        #     'time': datetime.utcnow().isoformat(),
        #     'event': 'reset_password',
        #     'details': {
        #         'body': body,
        #         'status_code': response.status,
        #         'data': response.json()
        #     }
        # }
        # log_to_json(log_data)
        return {'error': 'Failed to fetch data', 'status_code': response.status}

def educations(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/educations/"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    if response.status_code == 200:
        return response
    else:
        return 

def regions(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/regions"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    if response.status_code == 200:
        return response
    else:
        return 

def districts(token, district_id, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/districts/{district_id}"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    if response.status_code == 200:
        return response
    else:
        return 

#TODO bu ishlamidi
def upload_file(token, file_name, associated_with, usage, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant 
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
        response = requests.post(url, headers=default_header, files=files)
    return response








async def application_forms(token,birth_date,birth_place,citizenship,extra_phone,
                      first_name,last_name, gender,phone,photo,pin,serial_number,src,third_name,
                      is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
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
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            if response.status == 201:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to post request', 'status_code': response.status}


async def application_forms_transfer(token,country_id, direction_name,
                                     institution_name, transcript_file, which_course_now,
                                     is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'user_previous_education': {
            'country_id': country_id,
            'direction_name': direction_name,
            'institution_name': institution_name,
            'transcript_file': transcript_file,
            'which_course_now': which_course_now
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=default_header, json=body) as response:
            if response.status == 201:
                data = await response.json()
                return data
            else:
                return {'error': 'Failed to post request', 'status_code': response.status}


async def application_forms_me(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/me"
    default_header['Authorization'] = f'Bearer {token}'

    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                data = await response.json()
                return {'error': 'Failed to post request', 'status_code': response.status}

async def application_forms_me_new(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/me"
    default_header['Authorization'] = f'Bearer {token}'

    # return response
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_header) as response:
            if response.status == 200:
                data = await response.json()
                return {'data': data, 'status_code': response.status} #data
            else:
                return {'error': 'Failed to post request', 'status_code': response.status}


async def delete_profile(token, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/application-forms/delete-profile"
    headers = default_header.copy()
    headers['Authorization'] = f'Bearer {token}'
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 200:
                try:
                    return response.status
                except aiohttp.client_exceptions.ContentTypeError:
                    return {'error': 'Response content type is not application/json', 'status_code': response.status}
            else:
                return {'error': 'Failed to delete profile', 'status_code': response.status}

async def return_token_use_refresh(refreshToken, is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    url = f"https://{host}/v1/auth/refresh"
    body = {
        'refreshToken': refreshToken,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, body=body, headers=default_header) as response:
            if response.status == 201:
                data = await response.json()
                return data
            else:
                return {'error': response.text, 'status_code': response.status}

def upload_sertificate(token, filename, f_type):
    try:
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
        response = requests.post(url, json=body, headers=headers)
        return response.json()

    except:
        return {'error': 'Failed to upload sertificate', 'status_code': 500}
# u_s = upload_sertificate("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQ5LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci9jMjU3MmI1NS02MzA3LTQ3YTEtOGYzNy03NjZjMGFiYTE3ZjIuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTlUMDQ6NDA6NTMuMzkxWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTE5VDA0OjQwOjUzLjM5MVoiLCJ1bml2ZXJzaXR5SWQiOjIsImlhdCI6MTcxMzAyMjI3OCwiZXhwIjoxNzEzMDQzODc4fQ.v5vh5-y6W8jjdVS8jcUpTW1PO5YUBTTRDzWvt9qOxHE",
#                         'certificate/3b2167c7-28d2-4d0b-b69d-87da4d4db3c1.jpg',
#                          'ielts' )
# ic(u_s)



def application_forms_for_edu(token,  district_id, education_id, file_, institution_name, region_id,src='manually',
                              is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
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
    if response.status_code == 201:
        return response
    else:
        return {'error': 'Failed to create application', 'status_code': response.status}

def application_forms_for_personal_data(token,  birth_date, birth_place, citizenship, extra_phone, first_name,gender,last_name,phone,serial_number,third_name,
                                         is_grant_origin=False):
    if is_grant_origin:
        default_header['Origin'] = origin_grant
    try:
        url = f"https://{host}/v1/application-forms"
        default_header['Authorization'] = f"Bearer {token}"
        body = {
            'birth_date': birth_date,
            'birth_place': birth_place,
            'citizenship': citizenship,
            'extra_phone': extra_phone,
            'first_name': first_name,
            'gender': gender,
            'last_name': last_name,
            'phone': phone,
            'serial_number': serial_number,
            'src': 'manually',
            'third_name': third_name
        }
        response = requests.post(url, json=body, headers=default_header)
        return response
    except Exception as e:
        return {'error': f'Failed to create application: {e}', 'status_code': 500}


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
            ic(response.status)
            if response.status == 200:
                data = await response.json()
                # log_data = {
                #     'time': datetime.utcnow().isoformat(),
                #     'event': 'djtoken',
                #     'details': {
                #         'status_code': response.status,
                #         # 'data': data
                #     }
                # }
                # log_to_json(log_data)
                return data
            else:
                # log_data = {
                #     'time': datetime.utcnow().isoformat(),
                #     'event': 'djtoken',
                #     'details': {
                #         'status_code': response.status,
                #         # 'data': response.json()
                #     }
                # }
                # log_to_json(log_data)
                return {'error': 'Failed to get token', 'status_code': response.status}

# def create_user_profile(token,chat_id,first_name,last_name,pin,date,username,university_name):
#     url = f"https://{crm_django_domain}/create-user-profile/"
#     header = {
#         'Authorization': f'Bearer {token}'
#     } 
#     body = {
#         'chat_id_user': chat_id,
#         'first_name_user': first_name,
#         'last_name_user': last_name,
#         'pin': pin,
#         'username': username,
#         'date': date,
#         "university_name": university_name
#     }
#     # ic(body)
#     response = requests.post(url, json=body, headers=header)
#     if response.status_code == 201:
#         # log_data = {
#         #     'time': datetime.utcnow().isoformat(),
#         #     'event': 'create_user_profile',
#         #     'details': {
#         #         'status_code': response.status_code,
#         #         # 'data': response.json()
#         #     }
#         # }
#         return response.json()
#     else:
#         # log_data = {
#         #     'time': datetime.utcnow().isoformat(),
#         #     'event': 'create_user_profile',
#         #     'details': {
#         #         'status_code': response.status_code,
#         #         # 'data': response.text
#         #     }
#         # }
#         # log_to_json(log_data)
#         return {'error': 'Failed to create user profile', 'status_code': response.status_code}

import aiohttp
import asyncio

async def create_user_profile(token, chat_id, first_name, last_name, pin, date, username, university_name):
    url = f"https://{crm_django_domain}/create-user-profile/"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    body = {
        'chat_id_user': chat_id,
        'first_name_user': first_name,
        'last_name_user': last_name,
        'pin': pin,
        'username': username,
        'date': date,
        'university_name': university_name
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers, timeout=30) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    return {
                        'error': 'Failed to create user profile',
                        'status_code': response.status,
                        'detail': await response.text()
                    }

    except aiohttp.ClientError as e:
        return {
            'error': 'Request exception',
            'detail': str(e)
        }


# def update_user_profile(university_id, chat_id, phone, first_name, last_name, pin, username,date):
#     url = f"https://{crm_django_domain}/update-user-profile/{chat_id}/{university_id}/"
#     # ic(url)
#     body = {
#         'chat_id_user': chat_id,
#         'phone': phone,
#         'first_name_user': first_name,
#         'last_name_user': last_name if last_name else 'None',
#         'pin': pin,
#         'username': username,
#         'date': date,
#         'university_name': university_id
#     }
#     # ic(body)
#     response = requests.put(url, json=body)
#     if response.status_code == 200:
#         # log_data = {
#         #     'time': datetime.utcnow().isoformat(),
#         #     'event': 'update_user_profile',
#         #     'details': {
#         #         'status_code': response.status_code,
#         #         'data': response.json()
#         #     }
#         # }
#         return response.json()
#     else:
#         # log_data = {
#         #     'time': datetime.utcnow().isoformat(),
#         #     'event': 'update_user_profile',
#         #     'details': {
#         #         'status_code': response.status_code,
#         #         'data': response.json()
#         #     }
#         # }
#         # log_to_json(log_data)
#         return response.json()

import aiohttp
import asyncio

async def update_user_profile(university_id, chat_id, phone, first_name, last_name, pin, username, date):
    url = f"https://{crm_django_domain}/update-user-profile/{chat_id}/{university_id}/"
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'chat_id_user': chat_id,
        'phone': phone,
        'first_name_user': first_name,
        'last_name_user': last_name if last_name else 'None',
        'pin': pin,
        'username': username,
        'date': date,
        'university_name': university_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers, timeout=20) as response:
                response_data = await response.json()
                return response_data
    except aiohttp.ClientError as e:
        return {
            'error': 'Request exception',
            'detail': str(e)
        }

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
                # log_data = {
                #     'time': datetime.utcnow().isoformat(),
                #     'event': 'get_all_ser_profile',
                #     'details': {
                #         'status_code': response.status,
                #         'data': data
                #     }
                # }
                # log_to_json(log_data)
                return data
            else:
                # log_data = {
                #     'time': datetime.utcnow().isoformat(),
                #     'event': 'get_all_ser_profile',
                #     'details': {
                #         'status_code': response.status,
                #         'data': response.json()
                #     }
                # }
                # log_to_json(log_data)
                return {'error': 'Failed to fetch data', 'status_code': response.status}

def get_user_profile(chat_id,university_id):
    url = f"https://{crm_django_domain}/detail-user-profile/{int(chat_id)}/{int(university_id)}/"
    response = requests.get(url)
    # ic(response.status_code, response.json())
    if response.status_code == 200:
        # log_data = {
        #     'time': datetime.utcnow().isoformat(),
        #     'event': 'get_user_profile',
        #     'details': {
        #         'status_code': response.status_code,
        #         'data': response.json()
        #     }
        # }
        # log_to_json(log_data)
        return response.json()
    else:
        # log_data = {
        #     'time': datetime.utcnow().isoformat(),
        #     'event': 'get_user_profile',
        #     'details': {
        #         'status_code': response.status_code,
        #         'data': response.json()
        #     }
        # }
        # log_to_json(log_data)
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}
    



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
            # print(resp.status)  # Using print for simplicity
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
    try:
        datetime_obj_utc = datetime.strptime(iso_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        your_timezone = pytz.timezone("Asia/Tashkent")
        datetime_obj_local = datetime_obj_utc.replace(tzinfo=pytz.utc).astimezone(your_timezone)
        return datetime_obj_local.strftime("%Y-%m-%d")

    except:
        return "vaqt topilmadi"

def convert_time_new(iso_datetime_str):
    try:
        datetime_obj_utc = datetime.strptime(iso_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        your_timezone = pytz.timezone("Asia/Tashkent")
        datetime_obj_local = datetime_obj_utc.replace(tzinfo=pytz.utc).astimezone(your_timezone)
        return datetime_obj_local
    except:
        return "vaqt topilmadi"


async def countries(token):
    url = "https://crmapi.mentalaba.uz/v1/application-forms/countries"
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
            import aiohttp




async def grant_directions(token, degree_id=1, education_type_id=1, admission_status="active", education_language_id=1, timeout_sec=10):
    BASE_URL = "https://crmapi.mentalaba.uz/v1/admissions/filter/select-box/directions"
    params = {
        "degree_id": degree_id,
        "education_type_id": education_type_id,
        "admission_status": admission_status,
        "education_language_id": education_language_id
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = BASE_URL

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout_sec)) as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Successfully fetched grant directions.")
                    return data
                else:
                    logger.error(f"Failed to fetch data. Status: {response.status}")
                    return {
                        "error": "Failed to fetch data",
                        "status_code": response.status
                    }
    except asyncio.TimeoutError:
        logger.error("Request timed out.")
        return {"error": "Request timed out"}
    except aiohttp.ClientError as e:
        logger.error(f"HTTP request failed: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return {"error": f"Unexpected error: {str(e)}"}





async def grant_languages(token, degree_id=1, education_type_id=1, admission_status="active", timeout_sec=10):
    BASE_LANGUAGES_URL = "https://crmapi.mentalaba.uz/v1/admissions/filter/select-box/education_languages"
    
    params = {
        "degree_id": degree_id,
        "education_type_id": education_type_id,
        "admission_status": admission_status
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout_sec)) as session:
            async with session.get(BASE_LANGUAGES_URL, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Successfully fetched education languages.")
                    return data
                else:
                    logger.error(f"Failed to fetch data. Status: {response.status}")
                    return {
                        "error": "Failed to fetch data",
                        "status_code": response.status
                    }
    except asyncio.TimeoutError:
        logger.error("Request timed out.")
        return {"error": "Request timed out", "status_code": 408}
    except aiohttp.ClientError as e:
        logger.error(f"HTTP request failed: {e}")
        return {"error": str(e), "status_code": 500}
    except Exception as e:
        logger.exception("Unexpected error occurred.")
        return {"error": f"Unexpected error: {str(e)}", "status_code": 500}


def return_secret_code():
    random_code = random.randint(100000, 999999)
    return random_code


def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])


def convert_time(timestamp):
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "vaqt topilmadi"

def escape_markdown2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)





def save_chat_id(chat_id,firstname, lastname,bot_id,username,status):
    url = "https://ads.misterdev.uz/users/post"
    data = {
        "chat_id": chat_id,
        "firstname": firstname if firstname else "firstname not found",
        "lastname": lastname if lastname else "lastname not found",
        "bot_id": bot_id,
        "username": username if username else "username not found",
        "status": status
        }
    ic(data)
    response = requests.post(url, json=data)
    
    return response.json()

def update_user(id, chat_id,firstname, lastname,bot_id,username,status,created_at):
    url = f"https://ads.misterdev.uz/users/put/{id}"
    data = {
        "chat_id": chat_id,
        "firstname": firstname if firstname else "firstname not found",
        "lastname": lastname if lastname else "lastname not found",
        "bot_id": bot_id,
        "username": username if username else "username not found",
        "status": status,
        'created_at': created_at
        }
    ic(data)
    response = requests.put(url, json=data)
    return response.json()

def get_all_bots():
    url = "https://ads.misterdev.uz/bots/get"
    response = requests.get(url)
    return response.json()

def get_all_users():
    url = "https://ads.misterdev.uz/users/get"
    response = requests.get(url)
    
    return response.json()


