# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Poll, Choice, PollPost
from opps.core.admin import PublishableAdmin
from opps.core.admin import apply_opps_rules

from opps.core.widgets import OppsEditor
from opps.images.generate import image_url


class PollAdminForm(forms.ModelForm):
    class Meta:
        model = Poll
        widgets = {"headline": OppsEditor()}


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
                image_url(obj.image.archive.url, width=60, height=60))
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
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', 'channel', 'date_available',
                    'date_end', 'published', 'preview_url']
    list_filter = ["date_end", "date_available", "published", "channel"]
    search_fields = ["title", "headline"]
    exclude = ('user',)
    raw_id_fields = ['main_image', 'channel']
    inlines = [ChoiceInline, PollPostInline]
    readonly_fields = ['image_thumb']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug')}),
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

admin.site.register(Poll, PollAdmin)
