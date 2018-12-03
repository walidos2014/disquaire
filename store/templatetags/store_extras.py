from django import template

register = template.Library()

def currency(valeur, deci):
    return "{:,.{}f}".format(valeur, deci).replace(',', ' ').replace('.', ',')

register.filter('currency', currency)