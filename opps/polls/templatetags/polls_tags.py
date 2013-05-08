# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils import timezone
from opps.polls.models import Poll, PollBox, PollConfig

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poll(context, slug, relation='channel', template_name=None):
    """
    {% get_poll 'channel_slug' relation='channel' %}
    {% get_poll 'post_slug' relation='post' %}
    """

    poll = None
    t = template.loader.get_template('polls/poll_detail_ajax.html')
    if template_name:
        t = template.loader.get_template(template_name)

    # look in to config check if there is a poll configured for channel
    if relation == 'channel':
        """
        Config should be:
        key: poll_slug
        value: the-poll-slug
        channel: Channel (object)
        """
        poll_slug = PollConfig.get_value('poll_slug', channel__slug=slug)
        # get latest poll for the channel
        try:
            poll = Poll.objects.filter(
                channel__slug=slug,
                published=True,
                date_available__lte=timezone.now()
            ).latest('date_insert')
        except Poll.DoesNotExist:
            poll = []
        if poll_slug:
            try:
                poll = Poll.objects.filter(
                    slug=poll_slug,
                    channel__slug=slug,
                    published=True,
                    date_available__lte=timezone.now()
                ).latest('date_insert')
            except Poll.DoesNotExist:
                poll = []
    elif relation == 'post':
        try:
            poll = Poll.objects.filter(
                posts__slug=slug,
                published=True,
                date_available__lte=timezone.now()
            ).latest('date_insert')
        except Poll.DoesNotExist:
            poll = []
    return t.render(template.Context({'poll': poll, 'context': context}))


@register.simple_tag
def get_active_polls(number=5, channel_slug=None,
                     template_name='polls/actives.html'):

    active_polls = Poll.objects.all_opened()
    if channel_slug:
        active_polls = active_polls.filter(channel__slug=channel_slug)

    active_polls = active_polls[:number]

    t = template.loader.get_template(template_name)

    return t.render(template.Context({'active_polls': active_polls,
                                      'channel_slug': channel_slug,
                                      'number': number}))


@register.simple_tag(takes_context=True)
def get_pollbox(context, slug=None, channel_slug=None,
                template_name='polls/pollbox_detail.html',
                **kwargs):

    if slug and channel_slug:
        slug = u"{0}-{1}".format(slug, channel_slug)

    lookup = dict(
        site=settings.SITE_ID,
        date_available__lte=timezone.now(),
        published=True
    )

    if slug:
        # get the first box with specific slug
        lookup['slug'] = slug
    elif channel_slug:
        # get the first box of a channel
        lookup['channel_long_slug'] = channel_slug

    box = PollBox.objects.filter(**lookup)

    if box:
        box = box.latest('date_available')
    else:
        box = None

    t = template.loader.get_template(template_name)

    inner_context = {
        'pollbox': box,
        'slug': slug,
        'context': context
    }
    if kwargs:
        inner_context.update(kwargs)

    return t.render(template.Context(inner_context))


@register.simple_tag
def get_all_pollbox(channel_slug, template_name=None):
    boxes = PollBox.objects.filter(site=settings.SITE_ID,
                                   date_available__lte=timezone.now(),
                                   published=True,
                                   channel__slug=channel_slug)

    t = template.loader.get_template('polls/pollbox_list.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'pollboxes': boxes}))
