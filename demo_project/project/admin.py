# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Project, Planning, Tender, TenderItem, Milestone, Transaction

admin.site.register(Project)
admin.site.register(Planning)
admin.site.register(Tender)
admin.site.register(TenderItem)
admin.site.register(Milestone)
admin.site.register(Transaction)