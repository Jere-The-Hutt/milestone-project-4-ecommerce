from django import template


register = template.Library()


@register.filter
def truncate_before(value, keyword):
    if keyword in value:
        return value.split(keyword)[0].strip()
    return value
