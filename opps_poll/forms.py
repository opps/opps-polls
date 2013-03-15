#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class SingleChoiceForm(forms.Form):

    def __init__(self, choices, *args, **kwargs):
        super(SingleChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.ChoiceField(widget=forms.widgets.RadioSelect,
            choices=[(choice.id, choice.choice) for choice in choices])

    def save(self):
        pass

class MultipleChoiceForm(forms.Form):

    def __init__(self, choices, *args, **kwargs):
        super(MultipleChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
            choices=[(choice.id, choice.choice) for choice in choices])

    def save(self):
        pass