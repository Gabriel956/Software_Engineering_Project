from django import template
register = template.Library()

# Template filter to get item from dictionary by key
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
