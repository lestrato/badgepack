from django import template
register = template.Library()
from django.apps import apps

@register.filter
def instances(community, user):
    bi = apps.get_model('badge', 'BadgeInstance')
    badge_instances = bi.objects.filter(
        badge_class__community=community,
        earner=user,
    )
    #
    return badge_instances

@register.filter
def classes(community):
    bc = apps.get_model('badge', 'BadgeClass')
    badge_classes = bc.objects.filter(
        community=community,
        is_available=True,
    )
    #
    return badge_classes
