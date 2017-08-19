#!/usr/bin/env python3.6

import sys
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse


settings.configure(
    DEBUG=True,
    SECRET_KEY='secret',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


def home_page(request):
    return HttpResponse('Hello world')


urlpatterns = (
    url(r'^$', home_page),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


