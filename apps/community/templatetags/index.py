from django import template
register = template.Library()

@register.filter
def index(l, i):
    return l[i]
