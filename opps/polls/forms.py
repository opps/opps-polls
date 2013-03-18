#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .widgets import CheckboxSelectMultiple, RadioSelect


class SingleChoiceForm(forms.Form):

    def __init__(self, choices, display_choice_images=False, *args, **kwargs):
        super(SingleChoiceForm, self).__init__(*args, **kwargs)

        if display_choice_images:
            choices_list = [
              (choice.id, "<img src='{0}' > {1}".format(
                choice.image.image.url if choice.image else '#', choice.choice
                )) for choice in choices
            ]
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
            choices_list = [
              (choice.id, "<img src='{0}' > {1}".format(
                  choice.image.image.url if choice.image else '#', choice.choice
                  )) for choice in choices
            ]
        else:
            choices_list = [(choice.id, choice.choice) for choice in choices]

        self.fields['choices'] = forms.MultipleChoiceField(
                widget=CheckboxSelectMultiple,
                choices=choices_list
        )