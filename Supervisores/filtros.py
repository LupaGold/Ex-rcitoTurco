from django import template

register = template.Library()

@register.filter
def intersect(value, arg):
    return any(item in value for item in arg)