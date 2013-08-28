# -*- coding: utf-8 -*-

from django import template
from django.utils import timezone
from opps.polls.models import Poll

register = template.Library()


@register.simple_tag(takes_context=True)
def is_voted(context, poll):
    try:
        request = context['request']
        return 1 if poll.voted(request) else 0
    except:
        return 0


@register.simple_tag(takes_context=True)
def get_paginated(context, current, pages, template_name, limit):
    try:
        current = current - 1
        total = len(pages)
        has_more = (total - current) > limit
        pagination = {}

        if has_more:
            pagination['left'] = list(pages)[current:current + (limit / 2)]
            pagination['right'] = list(pages)[-((limit / 2) + (1 if limit % 2
                                                             else 0)):]
            pagination['more'] = current + (limit / 2) + 1
        else:
            pagination = pages
    except Exception:
        pagination = None

    t = None
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'pages': pages, 'pagination': pagination, 'context': context}))


@register.simple_tag(takes_context=True)
def get_poll(context, slug, template_name=None):
    """
    {% get_poll 'post_slug' template_name='polls/poll_in_post_detail.html' %}
    """

    try:
        poll = Poll.objects.filter(
            posts__slug=slug,
            published=True,
            date_available__lte=timezone.now()
        ).latest('date_insert')

        template_name = template_name or 'polls/poll_detail_ajax.html'
        t = template.loader.get_template(template_name)

        return t.render(template.Context({'poll': poll, 'context': context}))
    except Poll.DoesNotExist:
        return ""


@register.simple_tag(takes_context=True)
def get_active_polls(context, number=5, channel_slug=None,
                     template_name='polls/actives.html',
                     exclude_slug=None,
                     **kwargs):

    active_polls = Poll.objects.all_opened()
    if channel_slug:
        active_polls = active_polls.filter(channel__slug=channel_slug)

    if kwargs:
        active_polls = active_polls.filter(**kwargs)

    if exclude_slug:
        active_polls = active_polls.exclude(slug=exclude_slug)

    active_polls = active_polls[:number]

    t = template.loader.get_template(template_name)

    return t.render(template.Context({'active_polls': active_polls,
                                      'channel_slug': channel_slug,
                                      'number': number,
                                      'context': context}))
