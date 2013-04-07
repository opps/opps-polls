# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (Poll, Choice, PollPost, PollBox,
                     PollBoxPolls, PollConfig)

from opps.core.admin import PublishableAdmin

from redactor.widgets import RedactorEditor


class PollAdminForm(forms.ModelForm):
    class Meta:
        model = Poll
        widgets = {"headline": RedactorEditor()}


class ChoiceInline(admin.TabularInline):
    model = Choice
    fk_name = 'poll'
    raw_id_fields = ['image']
    action = None
    extra = 1
    fieldsets = [(None, {'fields': ('choice', 'image', 'order', 'votes')})]


class PollPostInline(admin.TabularInline):
    model = PollPost
    fk_name = 'poll'
    raw_id_fields = ['post']
    actions = None
    extra = 1
    classes = ('collapse',)


class PollAdmin(PublishableAdmin):
    form = PollAdminForm
    prepopulated_fields = {"slug": ["question"]}
    list_display = ['question', 'channel', 'date_available', 'date_end', 'published']
    list_filter = ["date_end", "date_available", "published", "channel"]
    search_fields = ["question", "headline"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']
    inlines = [ChoiceInline, PollPostInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('question', 'slug')}),
        (_(u'Content'), {
            'fields': ('headline', 'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', ('date_available', 'date_end'),
                       'order', 'multiple_choices', ('max_multiple_choices',
                       'min_multiple_choices'), ('display_choice_images',
                       'show_results'))}),
    )


class PollBoxPollsInline(admin.TabularInline):
    model = PollBoxPolls
    fk_name = 'pollbox'
    raw_id_fields = ['poll']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('poll', 'order')})]


class PollBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [PollBoxPollsInline]
    exclude = ('user',)
    raw_id_fields = ['channel', 'article']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': (('channel', 'article'),)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class PollConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]
    raw_id_fields = ['poll', 'channel', 'article']
    exclude = ('user',)


admin.site.register(Poll, PollAdmin)
admin.site.register(PollBox, PollBoxAdmin)
admin.site.register(PollConfig, PollConfigAdmin)
