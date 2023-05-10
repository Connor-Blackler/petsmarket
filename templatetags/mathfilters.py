from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def multiply(value, arg):
    """Multiplies the arg and the value"""
    return float(value) * float(arg)
