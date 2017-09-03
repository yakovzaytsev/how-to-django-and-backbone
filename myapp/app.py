#!/usr/bin/env python3.6

from datetime import datetime
import os
import sys
import django
from django.conf import settings
# next 3 lines what makes makemigrations work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path[0] = os.path.dirname(BASE_DIR)
APP_LABEL = os.path.basename(BASE_DIR)
settings.configure(
    DEBUG=True,
    SECRET_KEY='secret',
    ROOT_URLCONF=__name__,
    STATIC_URL = '/static/',
    STATICFILES_DIRS = [
        os.path.dirname(__file__),
    ],
    INSTALLED_APPS = (
        APP_LABEL,
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        # 'rest_framework',
        # 'rest_framework.authtoken',
        'channels',
    ),
    MIDDLEWARE_CLASSES= (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'myapp'
        }
    },
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgiref.inmemory.ChannelLayer',
            'ROUTING': f'{__name__}.channel_routing',
        }
    },
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.dirname(__file__)],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
)
django.setup()
from django.conf.urls import include, url
from django.core.wsgi import get_wsgi_application
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from channels.routing import route
from channels.handler import AsgiHandler, AsgiRequest
from rest_framework.authtoken.views import obtain_auth_token


class ModelRun(models.Model):
    name = models.TextField(unique=True, default='')
    start_time = models.DateTimeField(default=None)  # datetime.now?
    end_time = models.DateTimeField(default=None)
    class Meta:
        app_label = APP_LABEL


def home_page(request):
    return render(request, 'home.html')


def http_consumer(message):
    request = AsgiRequest(message)
    response = home_page(request)  # HttpResponse('Hello world! You asked for %s' % message.content['path'])
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet messages
    # both have a 'text' key for their textual data
    message.reply_channel.send({
        'text': f"text is {message.content['text']}",
    })


urlpatterns = (
    url(r'^$', home_page),
    # url(r'^api/token/', obtain_auth_token, name='api_token'),
)


channel_routing = [
    # # override Django view layeer and handles every HTTP request directly
    # route('http.request', f'{__name__}.http_consumer'),
    route('websocket.receive', ws_message),
]


application = get_wsgi_application()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


