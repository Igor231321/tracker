from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter()
def format_number(value):
    result = intcomma(round(value))
    return f"{result}"
