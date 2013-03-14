# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

from opps.core.models import Publishable
from opps.channel.models import Channel
from opps.image.models import Image


class Poll(Publishable):

    question = models.CharField(_(u"Question"), max_length=255)
    multiple_choices = models.BooleanField(_(u"Allow multiple choices"),
        default=False)

    slug = models.SlugField(_(u"URL"), max_length=150, unique=True,
                            db_index=True)

    headline = models.TextField(_(u"Headline"), blank=True)
    channel = models.ForeignKey(Channel, verbose_name=_(u"Channel"))

    main_image = models.ForeignKey(Image,
                                   verbose_name=_(u'Poll Image'), blank=True,
                                   null=True, on_delete=models.SET_NULL,
                                   related_name='poll_image')
    tags = TagField(null=True, verbose_name=_(u"Tags"))
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)
    position  = models.IntegerField(_(u"Position"), default=0)

    def __unicode__(self):
        return self.question


class Choice(models.Model):

    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255, null=False, blank=False)
    votes = models.IntegerField(null=True, blank=True, default=0)
    image = models.ForeignKey(Image,
                            verbose_name=_(u'Choice Image'), blank=True,
                            null=True, on_delete=models.SET_NULL,
                            related_name='choice_image')
    position  = models.IntegerField(_(u"Position"), default=0)

    def __unicode__(self):
        return self.choice
