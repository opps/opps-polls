# -*- coding: utf-8 -*-
from django import template
from opps.polls.models import Poll, PollBox

register = template.Library()

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

@register.simple_tag
def get_pollbox(slug, channel_slug=None, template_name=None):
    if channel_slug:
        slug = u"{0}-{1}".format(slug, channel_slug)

    try:
        box = PollBox.objects.get(site=settings.SITE_ID, slug=slug,
                                     date_available__lte=timezone.now(),
                                     published=True)
    except PollBox.DoesNotExist:
        box = None

    t = template.loader.get_template('polls/pollbox_detail.html')
    if template_name:
        t = template.loader.get_template(template_name)

    return t.render(template.Context({'pollbox': box, 'slug': slug}))


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
