from django import template

register = template.Library()


@register.filter
def split_first(value, arg):
    """Splits and returns the first value"""
    return value.split(arg)[0].capitalize()[:5]
