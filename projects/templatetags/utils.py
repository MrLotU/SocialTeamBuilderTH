from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def starts_with(value, arg):
    return value.startswith(arg)

@register.simple_tag
def create_query(n=None, s=None, f=None):
    if not n and not s and not f:
        return ''
    arr = []
    if n:
        arr.append(f'n={n}')
    if s:
        arr.append(f's={s}')
    if f:
        arr.append(f'f={f}')
    return '?' + '&'.join(arr)
