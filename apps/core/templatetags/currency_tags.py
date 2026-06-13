from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def fcfa(amount):
    try:
        val = float(amount)
        formatted = f"{val:,.0f}".replace(",", " ")
        return f"{formatted} FCFA"
    except (ValueError, TypeError):
        return "0 FCFA"
