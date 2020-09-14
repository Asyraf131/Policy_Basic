from django import template

register = template.Library()


@register.filter(name='dashURL')
def dashURL(value):
    return value.replace(' ', '-')
