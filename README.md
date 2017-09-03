# how-to-django-and-backbone

## Setup

- (pip install -r requirements.txt)

- create PostgreSQL database

    $ createdb -E UTF-8 how_to_django_and_backbone

- then apply the migrations

    $ python ui.py migrate

## How to run ui

    $ gunicorn ui --log-file=-

On OS X do

    $ echo 'backend: TkAgg' >>  ~/.matplotlib/matplotlibrc

to workaround matplotlib in virtualenv 




