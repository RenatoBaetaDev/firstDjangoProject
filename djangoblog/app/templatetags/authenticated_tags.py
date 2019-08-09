from django import template

register = template.Library()


@register.filter
def is_admin(request):
    return hasattr(request, 'user') and request.user.is_authenticated()
