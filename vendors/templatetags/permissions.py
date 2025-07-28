from django import template

register = template.Library()


@register.filter(name='vendor_pem')
def vendor_pem(user):
    return user.groups.filter(name='Vendor').exists()


@register.filter(name='buyer_pem')
def buyer_pem(user):
    return user.groups.filter(name='Buyer').exists()