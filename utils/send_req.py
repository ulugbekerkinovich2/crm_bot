import requests
from pprint import pprint
import mimetypes
import os
from data.config import domain_name, origin
# domain_name = 'crmapi.mentalaba.uz'
# origin = 'admission.mentalaba.uz'

default_header = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'origin': f'{origin}', 
}

def check_number(phone):

    url = f'https://{domain_name}/v1/auth/check'

    data = {
        "phone": phone
    }

    response = requests.post(url, headers=default_header, json=data)  # Include the headers here

    return response
# check_number('+998942559015')


def user_register(number):
    url = f"https://{domain_name}/v1/auth/register"
    body = {
        "phone": number
    }
    response = requests.post(url, json=body, headers=default_header)
    return response

# user_login('+998998359015')

def user_verify(secret_code, phone):
    url = f"https://{domain_name}/v1/auth/verify"
    body = {
        'phone' : phone,
        "code": secret_code
    }
    response = requests.post(url, json=body, headers=default_header)

    return response
    
# user_verify(175654, '+998998359015')

def user_login(phone):
    url = f"https://{domain_name}/v1/auth/login"
    body = {
        'phone': phone
    }
    response = requests.post(url, json=body, headers=default_header)
    # print(response.json())
    return response
# user_login('+998998359015')

def application_form_info(birth_date, document, token):
    url = f'https://{domain_name}/v1/application-forms/info'
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'birth_date': birth_date,
        'document': document
    }
    response = requests.post(url, json=body, headers=default_header)
    # pprint(response.json())
    return response

def application_form(token,birth_date,birth_place,citizenship,extra_phone,first_name,gender,last_name,phone,photo,pin,      serial_number,src,third_name):
    url = f"https://{domain_name}/v1/application-forms"
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

def directions(token):
    url = f'https://{domain_name}/v1/directions'
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response

def applicants(token, degree_id, direction_id, education_language_id, education_type_id, work_experience_document=None):
    url = f"https://{domain_name}/v1/applicants"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'degree_id': degree_id,
        'direction_id': direction_id,
        'education_language_id': education_language_id,
        'education_type_id': education_type_id,
        'work_experience_document': work_experience_document
    }
    response = requests.post(url, json=body, headers=default_header)
    return response.json()

def update_applicant(token, degree_id, direction_id, education_language_id, education_type_id, applicant_id):
    url = f"https://{domain_name}/v1/applicants/{applicant_id}"  # Assuming you need to specify which applicant to update
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

def my_applications(token):
    url = f"https://{domain_name}/v1/applicants/my-application"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response

def reset_password(phone, token):
    url = f"https://{domain_name}/v1/auth/resend-verify-code"
    default_header['Authorization'] = f'Bearer {token}'
    body = {
        'phone': phone
    }
    response = requests.post(url, json=body, headers=default_header)
    return response

def educations(token):
    url = f"https://{domain_name}v1/application-forms/educations/"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response

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
    url = f"https://{domain_name}/v1/application-forms/regions"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response

def districts(token, district_id):
    url = f"https://{domain_name}/v1/application-forms/districts/{district_id}"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    return response

def upload_file(url, token, file_path, associated_with='users', usage='diploma'):
    if os.path.getsize(file_path) > 5 * 1024 * 1024:
        return {'error': 'File size exceeds the 5MB limit.'}
    mime_type, _ = mimetypes.guess_type(file_path)
    allowed_mime_types = {
        'image/png',
        'image/jpeg',
        'image/jpg',
        'application/pdf'
    }
    if mime_type not in allowed_mime_types:
        return {'error': 'File format is not supported. Allowed formats: PNG, JPG, JPEG, PDF.'}
    filename = file_path.split('/')[-1]
    payload = {
        'associated_with': associated_with,
        'usage': usage
    }
    with open(file_path, 'rb') as f:
        files = {
            'file': (filename, f, mime_type)
        }
        default_header['Authorization'] = f'Bearer {token}'
        response = requests.post(url, headers=default_header, data=payload, files=files)
    return response

# def application_form(token, src, district_id, education_id, file_vs_format, institution_name, region_id):
    # url = f"https://{domain_name}/v1/application-forms"
    # default_header['Authorization'] = f'Bearer {token}'
    # body = {
    #     'src': src,
    #     'user_education': {
    #         'district_id': district_id,
    #         'education_id': education_id,
    #         'file': [f'{file_vs_format}'],
    #         'institution_name': institution_name,
    #         'region_id': region_id,
    #         'src': src
    #     }
    # }
    # response = requests.post(url, json=body, headers=default_header)
    # return response
def application_forms(token,birth_date,birth_place,citizenship,extra_phone,
                      first_name,last_name, gender,phone,photo,pin,serial_number,src,third_name):
    url = f"https://{domain_name}/v1/application-forms"
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

def application_forms_me(token):
    url = f"https://{domain_name}/v1/application-forms/me"
    default_header['Authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=default_header)
    # print(response.json())
    return response

# a =application_forms_me('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjQ5LCJmaXJzdF9uYW1lIjoiVUxVR-KAmEJFSyIsImxhc3RfbmFtZSI6IkVSS0lOT1YiLCJiaXJ0aF9kYXRlIjpudWxsLCJwaG9uZSI6Iis5OTg5OTgzNTkwMTUiLCJyb2xlIjoidXNlciIsImF2YXRhciI6ImF2YXRhci9lM2Q0OWJmNi0zNGExLTRhNzktYjZlNS04MWU1OTg3MDRkNWIuanBnIiwiZW1haWwiOm51bGwsImlzX3ZlcmlmeSI6dHJ1ZSwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTlUMDQ6NDA6NTMuMzkxWiIsInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTE5VDA0OjQwOjUzLjM5MVoiLCJ1bml2ZXJzaXR5SWQiOjIsImlhdCI6MTcxMjA0OTY5OCwiZXhwIjoxNzEyMDcxMjk4fQ.TnhaeCx0OPYgMLwaonkFDWOt_cqZlkzpPieJWN5tL3g')
# pprint(a.json())

def refresh(refreshToken):
    url = f"https://{domain_name}/v1/auth/refresh"
    body = {
        'refreshToken': refreshToken,
    }
    response = requests.post(url, json=body, headers=default_header)
    return response

