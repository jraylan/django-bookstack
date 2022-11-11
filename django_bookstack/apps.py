# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class DjangoBookstackConfig(AppConfig):
    name = 'django_bookstack'

    def ready(self):
        from . import templatetags
