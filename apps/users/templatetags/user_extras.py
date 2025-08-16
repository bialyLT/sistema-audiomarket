from django import template

register = template.Library()

@register.filter
def split(value, separator):
    """Filtro para dividir una cadena usando un separador"""
    if value:
        return value.split(separator)
    return []

@register.filter
def trim(value):
    """Filtro para eliminar espacios en blanco al inicio y final"""
    if value:
        return value.strip()
    return value
