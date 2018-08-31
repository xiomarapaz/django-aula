from django import template

register = template.Library()

# tag to get the value of a field by name in template
@register.simple_tag
def get_value_from_key(object, key):
    # is it necessary to check isinstance(object, dict) here?
    return object[key-1]

@register.simple_tag
def get_value_from_table(object, y, x):
    #Torna un valor de la taula
    return object[y-1][x-1]