# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from .models import Poll, Choice, PollPost

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
    fieldsets = [(None, {'fields': ('choice', 'image', 'position', 'votes')})]


class PollPostInline(admin.TabularInline):
    model = PollPost
    fk_name = 'poll'
    raw_id_fields = ['post']
    actions = None
    extra = 1
    classes = ('collapse',)


class PollAdmin(admin.ModelAdmin):
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
            'fields': ('published', 'date_available', 'date_end',
                'position', 'multiple_choices','max_multiple_choices',
                'min_multiple_choices','display_choice_images',
                'template_path','show_results')}),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.site = obj.channel.site if obj.channel else Site.objects.get(pk=1)
            if obj.user:
                pass
        except User.DoesNotExist:
            obj.user = request.user

        super(PollAdmin, self).save_model(request, obj, form, change)


admin.site.register(Poll, PollAdmin)