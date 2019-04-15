from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown2 import markdown

register = Library()

@register.filter
@stringfilter
def starts_with(value, arg):
    return value.startswith(arg)

@register.simple_tag
def create_query(n=None, s=None, f=None, m=None):
    if not n and not s and not f and not m:
        return ''
    arr = []
    if n:
        arr.append(f'n={n}')
    if s:
        arr.append(f's={s}')
    if f:
        arr.append(f'f={f}')
    if m:
        arr.append(f'm={m}')
    return '?' + '&'.join(arr)

@register.filter
def markdown_to_html(value):
    print(value)
    html_body = markdown(value)
    return mark_safe(html_body)
