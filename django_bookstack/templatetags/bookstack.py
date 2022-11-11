# -*- coding: utf-8 -*-
from django import template
from django_bookstack import bookstack
from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.base import FilterExpression, Variable
from django.template.loader import get_template
from django.utils.safestring import mark_safe
import re
import traceback

register = template.Library()


class BookstackWrapperNode(template.Node):
    def __init__(self, kind, object_id, using, template_name, nodelist_loop, template_error=TemplateSyntaxError('Invalid tag syntax')):
        self.kind = kind
        self.object_id = object_id
        self.using = using
        self.template_name = template_name
        self.nodelist = nodelist_loop
        self.template_error = template_error

    def render(self, context):
        nodelist = []
        template_name = self.template_name
        object_id = self.object_id
        using = self.using
        kind = self.kind

        template_name = Variable(template_name).resolve(context) or FilterExpression(
            template_name).resolve(context, ignore_failures=True) or re.sub(r'["\']', '', template_name)
        object_id = Variable(object_id).resolve(context) or FilterExpression(
            object_id).resolve(context, ignore_failures=True) or re.sub(r'["\']', '', object_id)
        using = Variable(using).resolve(context) or FilterExpression(using).resolve(
            context, ignore_failures=True) or re.sub(r'["\']', '', using)
        kind = Variable(kind).resolve(context) or FilterExpression(kind).resolve(
            context, ignore_failures=True) or re.sub(r'["\']', '', kind)
            
        with context.push():
            for node in self.nodelist:
                nodelist.append(node.render_annotated(context))

        if not template_name or not object_id or not using or not kind:
            return mark_safe(''.join(nodelist))

        if kind not in ['page', 'chapter', 'book', 'shelf']:
            raise self.template_error

        loaded_template = get_template(template_name)
        template_context = {
            'wrapped_content': mark_safe(''.join(nodelist)),
            'page_link': bookstack.get_element_link(kind, object_id, using)
        }

        return mark_safe(loaded_template.render(template_context))


@register.tag('bookstack')
def bookstack_wrapper(parser, token):
    """
    Wraps the content of the block in a bookstack wrapper.

    Usage:
        {% bookstack (page|chapter|book|shelve)> <element_id> [ template=<template_name>:str ] [ using=<bookstack_instance> ] %}
            <content>
        {% endbookstack %}
    
    Example:
        {% bookstack page "my_page" template="myapp/my_page_wrapper.html" %}
            <h1>My Page</h1>
            <p>This is my page.</p>
        {% endbookstack %}
    """

    template_error = TemplateSyntaxError(
        "'bookstack' statements should use the format "
        "'bookstack (page|chapter|book|shelf)> <element_id> [ template=<template_name>:str ] [ using=<bookstack_instance> ]': %s"
        % token.contents)
    bits = token.split_contents()

    if len(bits) > 5 or len(bits) < 3:
        raise template_error

    template_name = "django_bookstack/bookstack_wrapper.html"
    kind = bits[1]
    object_id = bits[2]
    using = 'default'

    for arg in bits[3:]:
        if arg.startswith('using='):
            using = arg.split('=')[1]
            if not using:
                raise template_error
            continue
        elif arg.startswith('template='):
            template_name = arg.split('=')[1]
            if not template_name:
                raise template_error
            continue
        raise template_error

    nodelist_loop = parser.parse(('empty', 'endbookstack',))
    token = parser.next_token()

    if token.contents == 'empty':
        parser.parse(('endbookstack',))
        parser.delete_first_token()

    return BookstackWrapperNode(kind, object_id, using, template_name, nodelist_loop, template_error=template_error)
