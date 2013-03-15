#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from itertools import chain
from django.forms import CheckboxInput
from django.utils.html import format_html, format_html_join
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text, python_2_unicode_compatible

class CheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        id_ = final_attrs.get('id', None)
        output = ['<ul>']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
                label_for = format_html(' for="{0}_{1}"', id_, i)
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = format_html(option_label)
            output.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      label_for, rendered_cb, option_label))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class RadioInput(forms.widgets.RadioInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = format_html(self.choice_label)
        return format_html('<label{0}>{1} {2}</label>', label_for, self.tag(), choice_label)


@python_2_unicode_compatible
class RadioFieldRenderer(object):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """

    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return RadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return format_html('<ul>\n{0}\n</ul>',
                           format_html_join('\n', '<li>{0}</li>',
                                            [(force_text(w),) for w in self]
                                            ))


class RadioSelect(forms.widgets.Select):
    renderer = RadioFieldRenderer

    def __init__(self, *args, **kwargs):
        # Override the default renderer if we were passed one.
        renderer = kwargs.pop('renderer', None)
        if renderer:
            self.renderer = renderer
        super(RadioSelect, self).__init__(*args, **kwargs)

    def subwidgets(self, name, value, attrs=None, choices=()):
        for widget in self.get_renderer(name, value, attrs, choices):
            yield widget

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None: value = ''
        str_value = force_text(value) # Normalize to string.
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        return self.renderer(name, str_value, final_attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return self.get_renderer(name, value, attrs, choices).render()

    def id_for_label(self, id_):
        # RadioSelect is represented by multiple <input type="radio"> fields,
        # each of which has a distinct ID. The IDs are made distinct by a "_X"
        # suffix, where X is the zero-based index of the radio field. Thus,
        # the label for a RadioSelect should reference the first one ('_0').
        if id_:
            id_ += '_0'
        return id_