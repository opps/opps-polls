#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from opps.channel.models import Channel
from opps_poll.models import Poll, Choice


class PollList(ListView):

    context_object_name = "context"

    @property
    def template_name(self):
        return 'opps_poll/pool_list.html'

    @property
    def queryset(self):
        return Poll.objects.all_published()



class ChannelPollList(ListView):

    context_object_name = "context"

    @property
    def template_name(self):
        long_slug = self.kwargs.get('channel__long_slug')
        return 'opps_poll/{0}.html'.format(long_slug)

    @property
    def queryset(self):
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, long_slug=long_slug)
        return Poll.objects.filter(channel__long_slug=long_slug).all_published()



class PollDetail(DetailView):

    context_object_name = "context"

    @property
    def template_name(self):
        homepage = Channel.objects.get_homepage()
        if not homepage:
            return None
        long_slug = self.kwargs.get('channel__long_slug', homepage.long_slug)
        return 'opps_poll/{0}/{1}.html'.format(long_slug, self.kwargs['slug'])

    @property
    def queryset(self):
        get_object_or_404(Poll, slug=self.kwargs['slug'], published=True)
        return Poll.objects.filter(slug=self.kwargs['slug'], published=True).all()
