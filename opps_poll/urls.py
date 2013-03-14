#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url

from opps_poll.views import PollDetail, PollList


urlpatterns = patterns(
    '',
    url(r'^$', PollList.as_view(), name='poll_list'),
    url(r'^(?P<channel__long_slug>[\w//-]+)/(?P<slug>[\w-]+)$',
        PollDetail.as_view(), name='open_poll'),
    url(r'^(?P<channel__long_slug>[\w//-]+)$', PollList.as_view(),
        name='channel_poll'),
)
