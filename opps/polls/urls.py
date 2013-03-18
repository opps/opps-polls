#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from django.conf.urls import patterns, url

from .views import PollDetail, PollList, ChannelPollList


urlpatterns = patterns(
    '',
    url(r'^$', PollList.as_view(), name='list_poll'),
    url(r'^channel/(?P<channel__long_slug>[\w//-]+)$', ChannelPollList.as_view(),
        name='channel_poll'),
    url(r'^(?P<slug>[\w-]+)/(?P<result>[\w-]+)$',
        PollDetail.as_view(), name='result_poll'),
    url(r'^(?P<slug>[\w-]+)$',
        PollDetail.as_view(), name='open_poll'),

)
