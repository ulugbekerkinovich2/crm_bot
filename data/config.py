from environs import Env
from icecream import ic

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
ic(env.int("university_id"))
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
throttling_time = env.str("throttling_time")
domain_name = env.str("domain_name")
origin= env.str("origin")

ic(origin)
university_name_uz = env.str("university_name_uz")
university_name_ru = env.str("university_name_ru")
crm_django_domain = env.str("crm_django_domain")
username = env.str("username")
password = env.str("password")
university_id = 1
ic(university_id)