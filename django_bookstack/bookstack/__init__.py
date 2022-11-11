# -*- coding: utf-8 -*-
from django.urls import reverse
from django.conf.urls import url
from functools import update_wrapper
from .api import BookStackInstance


class Library(object):
    __instances = {}
    __urls = None
    
    def register_instance(self, instance, instance_namespace='default'):
        '''
        Register an instance of a bookstack under the namespace given by
        instance_namespace. If instance_namespace is not given, the default namespace
        will be used.
        Even if the first instance registered is not the default instance, the
        default instance will also be mapped to the first instance registered.

        :param instance: The instance of class BookStackInstance to be registered.
        :param instance_namespace: The namespace to register the instance (default: 'default')

        :returns: None
        
        '''
        assert isinstance(instance, BookStackInstance)
        
        if instance_namespace in self.__instances:
            raise ValueError("Instance name '%s' is already registered. Use replace_instance instead." % instance_namespace)
        instance.generate_api_methods()
        if 'default' not in self.__instances and instance_namespace != 'default':
            self.__instances['default'] = instance
        self.__instances[instance_namespace] = instance

    def replace_instance(self, instance, instance_namespace='default'):
        instance.generate_api_methods()
        self.__instances[instance_namespace] = instance

    def get_instance(self, instance_namespace='default'):
        return self.__instances[instance_namespace]

    def get_urls(self):
        if not self.__urls:
            from django_bookstack import views as django_bookstack_views
            self.__urls = [
                url(r'bookstack/pages/(?P<instance>[^/]+)/(?P<page_id>[1-9][0-9]*)/?$', django_bookstack_views.bookstack_page,
                    name='django_bookstack_page'),
                url(r'bookstack/chapters/(?P<instance>[^/]+)/(?P<chapter_id>[1-9][0-9]*)/?$', django_bookstack_views.bookstack_chapter,
                    name='django_bookstack_chapter'),
                url(r'bookstack/books/(?P<instance>[^/]+)/(?P<book_id>[1-9][0-9]*)/?$', django_bookstack_views.bookstack_book,
                    name='django_bookstack_book'),
                url(r'bookstack/shelves/(?P<instance>[^/]+)/(?P<shelf_id>[1-9][0-9]*)/?$', django_bookstack_views.bookstack_shelf,
                    name='django_bookstack_shelf'),
            ]
        return self.__urls


def get_element_link(kind, element_id, using='default'):
    '''
    Get the link to a bookstack element by it's id.
    '''
    if kind == 'page':
        return get_page_link(element_id, using)
    elif kind == 'chapter':
        return get_chapter_link(element_id, using)
    elif kind == 'book':
        return get_book_link(element_id, using)
    elif kind == 'shelf':
        return get_shelves_link(element_id, using)
    else:
        raise ValueError("Unknown bookstack element type: %s" % kind)


def get_page_link(page_id, using='default'):
    '''
    Return's a page reverse link using it's id

    Usage:
        get_page_link(shelf_id,using=instance_namespace)

    :param page_id: The page id
    :param using: (optional) The BookStack instance namespace. Default: 'default'

    :returns: str
    '''
    return reverse('django_bookstack_page', kwargs={'instance': using, 'page_id': page_id})


def get_chapter_link(chapter_id, using='default'):
    '''
    Return's a chapter reverse link using it's id

    Usage:
        get_chapter_link(shelf_id,using=instance_namespace)

    :param chapter_id: The chapter id
    :param using: (optional) The BookStack instance namespace. Default: 'default'

    :returns: str
    '''
    return reverse('django_bookstack_chapter', kwargs={'instance': using, 'chapter_id': chapter_id})


def get_book_link(book_id, using='default'):
    '''
    Return's a book reverse link using it's id

    Usage:
        get_book_link(shelf_id,using=instance_namespace)

    :param book_id: The book id
    :param using: (optional) The BookStack instance namespace. Default: 'default'

    :returns: str
    '''
    return reverse('django_bookstack_book', kwargs={'instance': using, 'book_id': book_id})


def get_shelves_link(shelf_id, using='default'):
    '''
    Return's a shelves reverse link using it's id

    Usage:
        get_shelves_link(shelf_id,using=instance_namespace)

    :param shelves_id: The shelves id
    :param using: (optional) The BookStack instance namespace. Default: 'default'

    :returns: str
    '''
    return reverse('django_bookstack_shelf', kwargs={'instance': using, 'shelf_id': shelf_id})


library = Library()



__all__ = (
    'library',
    'BookStackInstance',
)

