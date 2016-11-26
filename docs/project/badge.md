# Badge

Path: `/badgepack/apps/badge/`

## Admin
### BadgeClassAdmin
### BadgeInstanceAdmin

## Apps
None

## Fetches
Name | Description
--- | ---
`all_badge_classes(community)` | Returns BadgeClass objects for community `community`
`all_available_badge_classes(community)` | Returns available BadgeClass objects for community `community`
`a_badge_class(class_name)` | Return BadgeClass object with name `class_name` or None if it doesn't exist
`u_badge_instance(badgeclass, earner)` | Return BadgeInstance object with BadgeClass `badgeclass` and User `earner` or None if it doesn't exist

## Forms
Name | Fields
--- | ---
`BadgeCreationForm` | `image = forms.FileField`<br/>`name=forms.CharField`<br/>`description = forms.CharField`
`UserBadgeAssignForm` | `badge_assign = forms.CharField`
`OneBadgeAssignForm` | `badge_assign = forms.BooleanField`
`BadgeSetAvailabilityForm` | `availability = forms.CharField`

## Models
Name | Fields
--- | ---
`BadgeClass` | `name = models.CharField`<br/>`description = models.CharField`<br/>`image = models.ImageField`<br/>`slug = RandomSlugField`<br/>`community = models.ForeignKey`<br/>`creator = models.ForeignKey`<br/>`created_on = models.DateField`<br/>`is_available = models.BooleanField`<br/>`is_discontinued = models.BooleanField`<br/>`instances = models.ManyToManyField`
`BadgeClass` | `badge_class = models.ForeignKey`<br/>`earner = models.ForeignKey`<br/>`recieved_on = models.DateField`<br/>`assigned_by = models.ForeignKey`

## Templates

Name | Description
--- | ---
`badge.html` | Includable badge container

## Views
None
