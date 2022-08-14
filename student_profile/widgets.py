
from django import forms
from django.utils.safestring import mark_safe
from string import Template


class ImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        return mark_safe(Template(value).substitute())
