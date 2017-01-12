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

# Get all instances of a particular badge:
def all_badge_instances(badgeclass):
    try:
        badge_instance = BadgeInstance.objects.filter(
            badge_class=badgeclass
        )
    except BadgeInstance.DoesNotExist:
       badge_instance = None
    return badge_instance

# Get a list of badges and the number of instances within a community:
def community_badge_instance_counts(community):
    # Get available badges:
    avail = all_available_badge_classes(community=community)

    tmp = [[x, all_badge_instances(badgeclass=x).count()] for x in avail]
    instance_counts = sorted(tmp, key=lambda k: k[1])
    instance_counts.reverse()

    return instance_counts

# Get the number of badge instances belonging to a user in a community:
def u_badge_count(earner, community):
    num_badges = BadgeInstance.objects.filter(
        earner=earner,
        badge_class__community=community,
        badge_class__is_available=True,
    ).count()

    return num_badges

# Get all the badges owned by a user:
def u_all_badges(earner):
    try:
        all_badges = BadgeInstance.objects.filter(
            earner=earner,
            badge_class__is_available=True
        )
    except BadgeInstance.DoesNotExist:
        return None
    return all_badges