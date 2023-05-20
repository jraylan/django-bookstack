# Django BookStack

Django BookStack is a simple Django application that allows you to
interact with a BookStack API.

## Quick start

2.  Add \"django_bookstack\" to your INSTALLED_APPS settings like this:

``` python
# settings.py

INSTALLED_APPS = [
   ...,
   'django_bookstack',
]

```

3.  Configure some bookstack instance:

``` python 
#settings.py

from django_bookstack import bookstack

instance = bookstack.BookStackInstance(
    'https://bookstack.example.com',
    '*********** token id ***********',
    '********* token secret *********'
)
bookstack.library.register_instance(instance, 'instance_name')
```

4.  Include the django_bookstack URLconf in your project urls.py like
    this:

``` python
#urls.py

urlpatterns = [
    ...,
    path('/', include('django_bookstack.urls')),
]

```

5.  The content should be accessible at:

``` regex
/bookstack/(?P<type>books|pages|chapter|shelves)/(?P<instance_name>[^/]+)/(?P<object_id>[1-9][0-9]*)/?
```
