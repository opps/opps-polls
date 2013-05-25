#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from opps.channels.models import Channel
from .models import Poll
from .utils import CookedResponse

# IS THERE A BETTER WAY?
if not 'endless_pagination' in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS += (
        'endless_pagination',
    )


class PollList(ListView):

    context_object_name = "polls"

    @property
    def template_name(self):

        domain_folder = 'polls'
        if self.site.id > 1:
            domain_folder = "{0}/polls".format(self.site)

        return '{0}/poll_list.html'.format(domain_folder)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        return Poll.objects.all_published()


class ChannelPollList(ListView):

    context_object_name = "polls"

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage(site=self.site)
        if not homepage:
            return None

        long_slug = self.kwargs.get('channel__long_slug',
                                    homepage.long_slug)
        if homepage.long_slug != long_slug:
            long_slug = long_slug[:-1]

        domain_folder = 'polls'
        if self.site.id > 1:
            domain_folder = "{0}/polls".format(self.site)

        return '{0}/{1}.html'.format(domain_folder, long_slug)

    @property
    def queryset(self):
        self.site = get_current_site(self.request)
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, long_slug=long_slug)
        return Poll.objects.filter(
            channel__long_slug=long_slug,
            published=True,
            date_available__lte=timezone.now()
        )


class PollDetail(DetailView):

    context_object_name = "poll"
    model = Poll

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        names = []

        if self.voted:
            self.template_name_suffix = "_result"

        # decide if show results page
        if not self.object.is_opened and self.object.show_results:
            self.template_name_suffix = "_result"
        elif not self.object.is_opened:
            self.template_name_suffix = "_closed"

        if self.kwargs.get('result') and self.object.show_results:
            self.template_name_suffix = "_result"
        elif self.kwargs.get('result') and not self.object.show_results:
            self.template_name_suffix = "_closed"

        if self.request.is_ajax():
            self.template_name_suffix += "_ajax"

        if hasattr(self.object, '_meta'):
            app_label = self.object._meta.app_label
            object_name = self.object._meta.object_name.lower()
        elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
            app_label = self.model._meta.app_label
            object_name = self.model._meta.object_name.lower()

        if self.object.channel:
            long_slug = self.object.channel.long_slug

            # site specific template folder
            # sitename/polls/
            if self.site.id > 1:
                app_label = "{0}/{1}".format(self.site, app_label)

            # 1. try channel/poll template
            # opps_poll/channel-slug/poll-slug.html
            names.append('{0}/{1}/{2}.html'.format(
                app_label, long_slug, self.kwargs['slug']
            ))
            # 2. try a generic channel template
            # opps_poll/channel-slug/<model>_detail.html
            names.append('{0}/{1}/{2}{3}.html'.format(
                app_label, long_slug, object_name, self.template_name_suffix
            ))

        # 3. try poll template (all channels)
        # opps_poll/poll-slug.html
        names.append('{0}/{1}.html'.format(
            app_label, self.kwargs['slug']
        ))

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if hasattr(self.object, '_meta'):
            names.append("%s/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix
            ))
        elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
            names.append("%s/%s%s.html" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
                self.template_name_suffix
            ))

        return names

    def get_object(self):
        self.voted = False
        self.site = get_current_site(self.request)
        filters = dict(slug=self.kwargs['slug'], site=self.site)
        preview_enabled = self.request.user and self.request.user.is_staff
        if not preview_enabled:
            filters['date_available__lte'] = timezone.now()
            filters['published'] = True
        return get_object_or_404(Poll, **filters)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(PollDetail, self).get_context_data(**kwargs)

        #already voted send the voted object to template
        #if request.COOKIES.has_key(self.object.cookie_name):
        if self.object.cookie_name in request.COOKIES:
            choices = request.COOKIES[self.object.cookie_name]
            self.voted = context['voted'] = self.object.get_voted_choices(choices)

        if self.object.channel:
            context['channel'] = self.object.channel

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        # check if is_closed or not published
        # to deny votes
        if not self.object.is_opened or not self.object.published:
            context['error'] = _(u"Poll not opened for voting")
            return self.render_to_response(context)

        # check if already voted
        # if request.COOKIES.has_key(self.object.cookie_name):
        if self.object.cookie_name in request.COOKIES:
            context['error'] = _(u"You already voted on this poll")
            return self.render_to_response(context)

        # check if choices has been sent
        if not request.POST.get('choices'):
            context['error'] = _(u"You should select at least one option")
            return self.render_to_response(context)

        # check minimum and maximum choices
        if self.object.multiple_choices:
            try:
                choices_ids = request.POST.getlist('choices')
            except:
                choices_ids = (request.POST.get('choices'),)

            min_multiple_choices = self.object.min_multiple_choices
            max_multiple_choices = self.object.max_multiple_choices

            if min_multiple_choices and len(choices_ids) < min_multiple_choices:
                context['error'] = _(u"You should select at least %s options") % min_multiple_choices
                return self.render_to_response(context)

            if max_multiple_choices and len(choices_ids) > max_multiple_choices:
                context['error'] = _(u"You can select only %s options") % max_multiple_choices
                return self.render_to_response(context)

        self.voted = context['voted'] = self.object.vote(request)

        if self.voted:
            # set the cookie
            self.response_class = CookedResponse
            cookie_value = u"|".join([str(choice.pk) for choice in self.voted])
            cookie = (self.object.cookie_name, cookie_value)
            return self.render_to_response(context, cookie=cookie)

        return self.render_to_response(context)
