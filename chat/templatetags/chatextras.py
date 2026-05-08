from django import template
register=template.Library()

@register.filter(name='initials')
def initials(value):
    initials='' 
    a=value.split(' ')
    for name in a:
        if name and len(initials)<2:
            initials+=name[0].upper()

    return initials