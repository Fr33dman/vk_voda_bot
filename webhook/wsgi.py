# -*- coding: utf-8 -*-

import os,sys

#путь к проекту
sys.path.append('/home/f/fr33dman/vk_webhook/public_html')
#путь к фреймворку
sys.path.append('/home/f/fr33dman/vk_webhook')
#путь к виртуальному окружению
sys.path.append('/home/f/fr33dman/vk_webhook/public_html/venv/lib64/python2.7/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "webhook.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()