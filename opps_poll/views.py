#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from opps.channel.models import Channel
from opps_poll.models import Poll, Choice
from opps_poll.forms import SingleChoiceForm, MultipleChoiceForm


class PollList(ListView):

    context_object_name = "polls"

    @property
    def template_name(self):
        return 'opps_poll/pool_list.html'

    @property
    def queryset(self):
        return Poll.objects.all_published()



class ChannelPollList(ListView):

    context_object_name = "polls"

    @property
    def template_name(self):
        long_slug = self.kwargs.get('channel__long_slug')
        return 'opps_poll/{0}.html'.format(long_slug)

    @property
    def queryset(self):
        long_slug = self.kwargs['channel__long_slug'][:-1]
        get_object_or_404(Channel, long_slug=long_slug)
        return Poll.objects.filter(
               channel__long_slug=long_slug,
               published=True
            )



class PollDetail(DetailView):

    context_object_name = "poll"
    template_name_field = "template_path"
    model = Poll

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        names = []#super(PollDetail, self).get_template_names()

        if hasattr(self.object, '_meta'):
            app_label = self.object._meta.app_label
            object_name = self.object._meta.object_name.lower()
        elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
            app_label = self.model._meta.app_label
            object_name = self.model._meta.object_name.lower()

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if name:
                names.insert(0, name)

        # long_slug = self.kwargs.get('channel__long_slug')

        if self.object.channel:
            long_slug = self.object.channel.long_slug
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
        return get_object_or_404(Poll, slug=self.kwargs['slug'], published=True)

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = super(PollDetail, self).get_context_data(**kwargs)
    #     form = SingleChoiceForm()
    #     context['form'] = form
    #     return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print request.GET, request.POST
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
