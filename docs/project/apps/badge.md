# Backend
    work
    ├── apps
    │   ├── badge

## admin.py
* BadgeClassAdmin
* BadgeInstanceAdmin

## fetches.py
Name | Description
--- | ---
`all_badge_classes(community)` | **Returns**: BadgeClass objects for community `community`
`all_available_badge_classes(community)` | **Returns**: available BadgeClass objects for community `community`
`a_badge_class(class_name)` | **Returns**: BadgeClass object with name `class_name` or None if it doesn't exist
`u_badge_instance(badgeclass, earner)` | **Returns**: BadgeInstance object with BadgeClass `badgeclass` and User `earner` or None if it doesn't exist

## forms.py
Name | Description
--- | ---
`BadgeCreationForm` | **Fields**: image, name, description<br>**Functions**: none
`UserBadgeAssignForm` | **Fields**: badge_assign<br>**Functions**: none
`OneBadgeAssignForm` | **Fields**: badge_assign<br>**Functions**: none
`BadgeSetAvailabilityForm` | **Fields**: availability<br>**Functions**: none

## models.py
Name | Fields
--- | ---
`BadgeClass` | `name = models.CharField`<br/>`description = models.CharField`<br/>`image = models.ImageField`<br/>`slug = RandomSlugField`<br/>`community = models.ForeignKey`<br/>`creator = models.ForeignKey`<br/>`created_on = models.DateField`<br/>`is_available = models.BooleanField`<br/>`is_discontinued = models.BooleanField`<br/>`instances = models.ManyToManyField`
`BadgeInstance` | `badge_class = models.ForeignKey`<br/>`earner = models.ForeignKey`<br/>`recieved_on = models.DateField`<br/>`assigned_by = models.ForeignKey`

## tests.py
There doesn't seem to be anything here.

## views.py
There doesn't seem to be anything here.

---
# Frontend

    work
    ├── static
    │   ├── templates
    │   |   ├── badge

## templates
Name | Description
--- | ---
`badge.html` | A single badge (recommended to exist within a badge list; refer to `badge_list_sample.html` for sample usage)
`badge_list_sample.html` | Sample implementation of a badge list
