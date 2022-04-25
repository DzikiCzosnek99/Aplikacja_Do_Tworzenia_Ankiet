from django import template

register = template.Library()


@register.filter
def to_char(value):
    text = chr(96+value)
    text = text.upper()
    return text
