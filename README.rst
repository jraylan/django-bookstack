=====
Django BookStack
=====

Django BookStack is a simple Django application that allows you to interact
with a BookStack API.


Quick start
-----------

1. Add "django_bookstack" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_bookstack',
    ]

2. Include the django_bookstack URLconf in your project urls.py like this::

    path('bookstack/', include('django_bookstack.urls')),

3. Run ``python manage.py migrate`` to create the bookstack models.

