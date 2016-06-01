# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from opps.containers.models import Container
from opps.core.managers import PublishableManager

from .forms import MultipleChoiceForm, SingleChoiceForm


app_namespace = getattr(settings, 'OPPS_POLLS_URL_NAMESPACE', 'polls')


class PollManager(PublishableManager):

    def all_opened(self):
        return super(PollManager, self).get_query_set().filter(
            date_available__lte=timezone.now(),
            published=True
        ).filter(
            Q(date_end__gte=timezone.now()) | Q(date_end__isnull=True)
        )


class Poll(Container):

    multiple_choices = models.BooleanField(
        _(u"Allow multiple choices"),
        default=False
    )
    max_multiple_choices = models.PositiveIntegerField(
        _(u"Max number of selected choices"),
        blank=True,
        null=True
    )
    min_multiple_choices = models.PositiveIntegerField(
        _(u"Min number of selected choices"),
        blank=True,
        null=True
    )
    display_choice_images = models.BooleanField(
        _(u"Display Choice images"),
        default=False
    )
    headline = models.TextField(_(u"Headline"), blank=True)
    posts = models.ManyToManyField(
        'articles.Post', null=True, blank=True,
        related_name='poll_post',
        through='PollPost',
        verbose_name=_(u'Posts'),
    )
    date_end = models.DateTimeField(_(u"End date"), null=True, blank=True)
    order = models.IntegerField(_(u"Order"), default=0)
    show_results = models.BooleanField(_(u"Show results page"), default=True)

    @property
    def is_opened(self):
        now = timezone.now()
        self.date_available = self.date_available or now
        if not self.date_end and self.date_available <= now:
            return True
        elif not self.date_end and self.date_available > now:
            return False
        return now >= self.date_available and now <= self.date_end

    @property
    def choices(self):
        return self.choice_set.all()

    @property
    def cookie_name(self):
        return "opps_poll_{0}".format(self.pk)

    def voted(self, request):
        if self.cookie_name in request.COOKIES:
            choices = request.COOKIES[self.cookie_name]
            return self.get_voted_choices(choices)
        else:
            return False

    @property
    def vote_count(self):
        return self.choices.aggregate(Sum('votes'))['votes__sum']

    def get_voted_choices(self, choices):
        """
        receives a str separated by "|"
        returns a list of choices
        """
        choices_ids = [int(choice_id) for choice_id in choices.split("|")]
        return self.choice_set.filter(id__in=choices_ids)

    def form(self, *args, **kwargs):

        if self.multiple_choices:
            poll_form = MultipleChoiceForm
        else:
            poll_form = SingleChoiceForm

        return poll_form(
            self.choices,
            self.display_choice_images,
            *args,
            **kwargs
        )

    def vote(self, request):
        try:
            choices_ids = request.POST.getlist('choices')
        except:
            choices_ids = (request.POST.get('choices'),)

        choices = self.choice_set.filter(id__in=choices_ids)

        for choice in choices:
            choice.vote()
            choice.save()

        return choices

    def get_absolute_url(self):
        return reverse(
            '{0}:open_poll'.format(app_namespace),
            kwargs={'slug': self.slug}
        )

    def get_thumb(self):
        return self.main_image

    def clean(self):
        super(Poll, self).clean()
        repeated = Container.objects.filter(
            site=self.site,
            slug=self.slug,
        ).exclude(pk=self.pk)
        if repeated.exists():
            raise ValidationError(
                _(u"Already exists a Pool with same slug and site")
            )

    @property
    def search_category(self):
        return _("Poll")

    def __unicode__(self):
        return self.title

    objects = PollManager()

    class Meta:
        ordering = ['-date_available']
        verbose_name = _(u'Poll')
        verbose_name_plural = _(u'Polls')


class PollPost(models.Model):
    post = models.ForeignKey(
        'articles.Post',
        verbose_name=_(u'Poll Post'),
        null=True,
        blank=True,
        related_name='pollpost_post',
        on_delete=models.SET_NULL
    )
    poll = models.ForeignKey(
        'polls.Poll',
        verbose_name=_(u'Poll'),
        null=True,
        blank=True,
        related_name='poll',
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.poll.slug, self.post.slug)

    class Meta:
        verbose_name = _(u'Poll Post')
        verbose_name_plural = _(u'Polls Posts')


class Choice(models.Model):

    poll = models.ForeignKey('polls.Poll', verbose_name=_(u'Poll'))
    choice = models.CharField(max_length=255, null=False, blank=False,
                              verbose_name=_(u'Choice'))
    votes = models.IntegerField(null=True, blank=True, default=0,
                                verbose_name=_(u'Votes'))
    image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Choice Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='choice_image'
    )
    order = models.IntegerField(_(u"Order"), default=0)

    def __unicode__(self):
        return self.choice

    def vote(self):
        self.votes += 1

    @property
    def percentage(self):
        try:
            return float(self.votes) / float(self.poll.vote_count) * 100
        except ZeroDivisionError:
            return 0

    class Meta:
        ordering = ['order']
        verbose_name = _(u'Choice')
        verbose_name_plural = _(u'Choices')
