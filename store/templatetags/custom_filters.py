from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter(name='as_b')
def as_b(value):
    # Assuming `value` is a string with product details
    if isinstance(value, str):
        lines = value.split('\n')
        return ''.join([f'<p>{line.strip()}</p>' for line in lines if line.strip()])
    return value