import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

BOT_NAME = 'trends'

ROBOTSTXT_OBEY = True
