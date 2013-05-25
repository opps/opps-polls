# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .models import (Poll, Choice, PollPost, PollBox,
                     PollBoxPolls, PollConfig)

from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

from redactor.widgets import RedactorEditor
from opps.images.generate import image_url


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
    fieldsets = [(None, {'fields': ('choice', ('image', 'image_thumb'), 'order', 'votes')})]
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


class PollPostInline(admin.TabularInline):
    model = PollPost
    fk_name = 'poll'
    raw_id_fields = ['post']
    actions = None
    extra = 1
    classes = ('collapse',)


@apply_opps_rules('polls')
class PollAdmin(PublishableAdmin):
    form = PollAdminForm
    prepopulated_fields = {"slug": ["question"]}
    list_display = ['question', 'channel', 'date_available',
                    'date_end', 'published', 'preview_url']
    list_filter = ["date_end", "date_available", "published", "channel"]
    search_fields = ["question", "headline"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']
    inlines = [ChoiceInline, PollPostInline]
    readonly_fields = ['image_thumb']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'question', 'slug')}),
        (_(u'Content'), {
            'fields': ('headline', ('main_image', 'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', ('date_available', 'date_end'),
                       'order', 'multiple_choices', ('min_multiple_choices',
                       'max_multiple_choices'), 'display_choice_images',
                       'show_results')}),
    )


class PollBoxPollsInline(admin.TabularInline):
    model = PollBoxPolls
    fk_name = 'pollbox'
    raw_id_fields = ['poll']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('poll', 'order', 'date_available', 'date_end')})]


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
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def clean_ended_entries(self, request, queryset):
        now = timezone.now()
        for box in queryset:
            ended = box.pollboxpolls_pollboxes.filter(
                date_end__lt=now
            )
            if ended:
                ended.delete()
    clean_ended_entries.short_description = _(u'Clean ended polls')

    actions = ('clean_ended_entries',)


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
