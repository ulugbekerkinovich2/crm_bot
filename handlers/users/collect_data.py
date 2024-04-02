from utils import send_req
from pprint import pprint

def collect_me_data(token, field_name=None):
    print('token->', token)
    print('keldi serial_number: ', field_name)
    response = send_req.application_forms_me(token)
    data = response.json()
    print(response.json())
    
    # If field_name is not specified, return all data
    if field_name is None:
        return data
    
    # Search for the specified field_name
    try:
        if data[field_name] is not None:
            print('bor ekan', data[field_name])
            return data[field_name]
    except KeyError:
        print('topilmadi', data[field_name])
        return False
    
    
    # If field_name was specified but not found, you might want to return None or False
    # Depending on your use case, choose one:
    return None  # Indicates the field_name was not found in the data
    # return False  # Alternatively, return False to indicate the field was not found

            

    # application_id = data['application_id']
    # application_src = data['application_src']
    # user_education_src = data['user_education_src']
    # first_name = data['first_name']
    # last_name = data['last_name']
    # third_name = data['third_name']
    # photo = data['photo']
    # src = data['src']
    # serial_number = data['serial_number']
    # pin = data['pin']
    # birth_date = data['birth_date']
    # gender = data['gender']
    # which_level_need = data['which_level_need']
    # phone = data['phone']
    # extra_phone = data['extra_phone']
    # country_id = data['country_id']
    # country_name_uz = data['country_name_uz']
    # country_name_ru = data['country_name_ru']
    # country_name_en = data['country_name_en']
    # region_id = data['region_id']
    # region_name_uz = data['region_name_uz']
    # region_name_ru = data['region_name_ru']
    # region_name_en = data['region_name_en']
    # address = data['address']
    # father_name = data['father_name']
    # father_phone = data['father_phone']
    # mother_name = data['mother_name']
    # mother_phone = data['mother_phone']
    # birth_place = data['birth_place']
    # pinfl_birth_country = data['pinfl_birth_country']
    # pinfl_birth_country_id = data['pinfl_birth_country_id']
    # citizenship = data['citizenship']
    # created_at = data['created_at']
    # pinfl_user_education = data['pinfl_user_education']
    # user_education = data['user_education']
    # certifications = data['certifications']
    # haveApplicationForm = data['haveApplicationForm']
    # haveApplied = data['haveApplied']
    # haveEducation = data['haveEducation']
    # didTakeTheTest = data['didTakeTheTest']


            
    