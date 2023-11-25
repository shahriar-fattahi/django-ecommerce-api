from .base import *

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")

PNAME = os.environ.get("PNAME")
PUSER = os.environ.get("PUSER")
PPASSWORD = os.environ.get("PPASSWORD")
PHOST = os.environ.get("PHOST")
PPORT = os.environ.get("PPORT")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": PNAME,
        "USER": PUSER,
        "PASSWORD": PPASSWORD,
        "HOST": PHOST,
        "PORT": PPORT,
    }
}
