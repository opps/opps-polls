#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .widgets import CheckboxSelectMultiple, RadioSelect


def get_image_url(choice):
    url = "#"
    if choice.image:
        img = choice.image
        # backwards compatibility
        if getattr(img, 'image', False):
            url = img.image.url
        else:
            url = img.archive.url

    return url


class SingleChoiceForm(forms.Form):

    def __init__(self, choices, display_choice_images=False, *args, **kwargs):
        super(SingleChoiceForm, self).__init__(*args, **kwargs)

        if display_choice_images:
            choices_list = []
            for choice in choices:
                choices_list.append((choice.id,
                                     u"<img src='{0}' > {1}".format(
                                         get_image_url(choice),
                                         choice.choice)))
        else:
            choices_list = [(choice.id, choice.choice) for choice in choices]

        self.fields['choices'] = forms.ChoiceField(
            widget=RadioSelect,
            choices=choices_list
        )


class MultipleChoiceForm(forms.Form):

    def __init__(self, choices, display_choice_images=False, *args, **kwargs):
        super(MultipleChoiceForm, self).__init__(*args, **kwargs)

        if display_choice_images:
            choices_list = []
            for choice in choices:
                choices_list.append((choice.id,
                                     u"<img src='{0}' > {1}".format(
                                         get_image_url(choice),
                                         choice.choice)))
        else:
            choices_list = [(choice.id, choice.choice) for choice in choices]

        self.fields['choices'] = forms.MultipleChoiceField(
            widget=CheckboxSelectMultiple,
            choices=choices_list
        )
