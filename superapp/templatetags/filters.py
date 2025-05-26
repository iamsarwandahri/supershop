from django import template

register = template.Library()


@register.filter
def multiply(value, multiplyby):
    return round(float(value)*float(multiplyby), 2)


@register.filter
def mod(value, dividedby):
    if value % dividedby == 0:
        return True
    else:
        return False


@register.filter
def myrange(value):
    return range(value)


@register.filter
def addfloat(value, add):
    return round(float(value+add), 2)
