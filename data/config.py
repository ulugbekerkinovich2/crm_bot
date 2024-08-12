from environs import Env
from icecream import ic

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
print(BOT_TOKEN)
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
throttling_time = env.str("throttling_time")
domain_name = env.str("domain_name")
GROUP_CHAT_ID = env.str("GROUP_CHAT_ID")

# origin= env.str("origin") if env.str("origin") == "qabul.aifu.uz" else "qabul.aifu.uz"
origin= env.str("origin")
# origin= env.str("origin") if env.str("origin") == "admission.mentalaba.uz" else "admission.mentalaba.uz"
# origin= env.str("origin") if env.str("origin") == "192.168.100.28" else "192.168.100.28"


ic(origin)
university_name_uz = env.str("university_name_uz")
university_name_ru = env.str("university_name_ru")
crm_django_domain = env.str("crm_django_domain")
username = env.str("username")
password = env.str("password")
university_id = env.int("university_id")
university_id = int(env.str("university_id"))
web_app_url = env.str("web_app_url")
port= env.int("port")
university_site_url=env.str("university_site_url")
exam_link=env.str("exam_link")