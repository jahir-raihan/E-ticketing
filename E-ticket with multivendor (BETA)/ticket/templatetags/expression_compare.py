from django import template

register = template.Library()


@register.filter(name='equal_by_mod')
def is_equal_by_mod(number, mod_by):
    return True if number % mod_by == 0 else False
