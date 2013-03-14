#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url

from opps_poll.views import PollDetail, PollList, ChannelPollList


urlpatterns = patterns(
    '',
    url(r'^$', PollList.as_view(), name='poll_list'),
    url(r'^channel/(?P<channel__long_slug>[\w//-]+)$', ChannelPollList.as_view(),
        name='channel_poll'),
    url(r'^(?P<slug>[\w-]+)$',
        PollDetail.as_view(), name='open_poll'),

)
