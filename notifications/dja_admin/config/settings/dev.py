import os

from django.conf import settings
from dotenv import load_dotenv
from split_settings.tools import include

from .base import *

load_dotenv()

# Output Django SQL queries to cli logs
ECHO_SQL_QUERIES = os.getenv("ECHO_SQL_QUERIES", True) == "True"


if settings.DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    INTERNAL_IPS = ["127.0.0.1"]

    if ECHO_SQL_QUERIES:
        include("components/logger.py")
