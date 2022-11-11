# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.cache import cache_page
from django_bookstack.bookstack import utils
import traceback


def cached(view):
    '''
    Wraps a view into `cache_page` by the time set in `DJANGO_BOOKSTACK_CACHE_TIMEOUT`.
    If the config is not set it will cache the view for 300 seconds.
    If the config is set to <= 0 or a not int value it will not cache the view.
    '''
    cache_timeout = getattr(settings, 'DJANGO_BOOKSTACK_CACHE_TIMEOUT', 300)
    if isinstance(cache_timeout, int) and cache_timeout > 0:
        return cache_page(cache_timeout)(view)
        
    return view


@cached
def bookstack_page(request, instance, page_id):
    try:
        page_html = utils.get_page_by_id(page_id, instance)
    except:
        traceback.print_exc()
        return HttpResponseNotFound()
    return HttpResponse(page_html)


@cached
def bookstack_chapter(request, instance, chapter_id):
    try:
        chapter_html = utils.get_chapter_by_id(chapter_id, instance)
    except:
        traceback.print_exc()
        return HttpResponseNotFound()
    return HttpResponse(chapter_html)


@cached
def bookstack_book(request, instance, book_id):
    try:
        book_html = utils.get_book_by_id(book_id, instance)
    except:
        traceback.print_exc()
        return HttpResponseNotFound()
    return HttpResponse(book_html)


@cached
def bookstack_shelf(request, instance, shelf_id):
    try:
        shelf_html = utils.get_shelf_by_id(shelf_id, instance)
    except:
        traceback.print_exc()
        return HttpResponseNotFound()
    return HttpResponse(shelf_html)

