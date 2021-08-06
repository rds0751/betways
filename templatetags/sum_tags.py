from django import template

register = template.Library()

@register.simple_tag()
def sum(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return float(qty) + float(unit_price)

@register.simple_tag()
def mul(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return float(qty) * float(unit_price)

@register.simple_tag()
def div(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return float(qty) / float(unit_price)

@register.simple_tag()
def sub(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return float(qty) - float(unit_price)