from community.models import Community
from badge.models import BadgeClass, BadgeInstance

def all_badge_classes(community):
    all_badges = BadgeClass.objects.filter(
        community=community
    )
    return all_badges

def all_available_badge_classes(community):
    all_badges = BadgeClass.objects.filter(
        community=community,
        is_available=True,
    )
    return all_badges


def a_badge_class(class_name):
    # user badge class return it or none
    try:
        badge_class = BadgeClass.objects.get(
            name=class_name,
        )
    except BadgeClass.DoesNotExist:
       badge_class = None
    return badge_class

def u_badge_instance(badgeclass, earner):
    # user badge instance return it or none
    try:
        badge_instance = BadgeInstance.objects.get(
            badge_class=badgeclass,
            earner=earner
        )
    except BadgeInstance.DoesNotExist:
       badge_instance = None
    return badge_instance
