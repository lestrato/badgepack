# Community

Path: `/badgepack/community/`

# Templates

Name | Description
--- | ---
`community.html` | Base template for all community pages
`earner.html` | Community page as-seen by regular (non-moderator) members
`moderator.html` | Community page as-seen by community moderators
`visitor.html` | Community page as-seen by non-members of the community

# Admin

# Forms

# Models
## Community

### Model

Name | Field | Settings | Description
--- | --- | --- | ---
`name` | `CharField` | `max_length=20`<br/>`unique=True` | Name of the community
`description` | `TextField` | | Description of the community
`tag` | `CharField` | `max_length=10` | Community tag (what the community is listed as in the navigation bar)
`is_private` | `BooleanField` | `default=False` | Whether or not users can join the community freely (if false, users must be invited / approved)
`created_on` | `DateField` | `default=datetime.now` | Date and time this community was created
`members` | `ManyToManyField` | `through='Membership'`<br/>`related_name='community_members'`<br/>`through_fields=('community', 'user')` | Set of community members
`invitations` | `ManyToManyField` | `through='Invitation'`<br/>`related_name='community_invitations'`<br/>`through_fields=('community', 'recipient')` | Set of community invitations
`applications` | `ManyToManyField` | `through='Application'`<br/>`related_name='community_applications'`<br/>`through_fields=('community', 'applicant')` | Set of community applications

### Meta

Field | Value
--- | ---
`verbose_name` | `'community'`
`verbose_name_plural` | `'communities'`
`db_table` | `'community'`

### Methods

Method | Description
--- | ---
`__str__(self)` | Returns the name of the community

## Membership

Intermediary table between communities and users.
    
### Model

Name | Field | Settings | Description
--- | --- | --- | ---
`user` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE` | A user who is a member of the community
`community` | `ForeignKey` | `Community`<br/>`on_delete=models.CASCADE` | The community that the user is a member of
`joined_on` | `DateField` | `default=datetime.now` | Date and time the user joined the community
`is_moderator` | `BooleanField` | `default=False` | Whether or not a user is a moderator of a community

### Meta

Field | Value
--- | ---
`verbose_name` | `'membership'`
`verbose_name_plural` | `'memberships'`
`db_table` | `'membership'`

### Methods

Method | Description
--- | ---
`__str__(self)` | Returns the user's username

## AbstractRequest

Community requests (invitations and applications).

### Model

Name | Field | Settings | Description
--- | --- | --- | ---
`community` | `ForeignKey` | `Community`<br/>`on_delete=models.CASCADE`<br/> | The community involved in the request
`created_on` | `DateField` | `default=datetime.now` | The date and time that the request was made

### Meta

Field | Value
--- | ---
`abstract` | `True`

## Invitation

### Model

Name | Field | Settings | Description
--- | --- | --- | ---
`recipient` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='invitation_recipient'` | The user who received the invitation
`sender` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='invitation_sender'` | The moderator who sent the invitation


### Meta

Field | Value
--- | ---
`verbose_name` | `invitation`
`verbose_name_plural` | `invitations`
`db_table` | `invitation`

### Methods

Method | Description
--- | ---
`__str__(self)` | Returns the recipient's username

## Application

### Model

Name | Field | Settings | Description
--- | --- | --- | ---
`accepted_by` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='application_accepted_by'` | The moderator who accepted the application
`applicant` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='application_applicant'` | The user who submitted the application


### Meta

Field | Value
--- | ---
`verbose_name` | `application`
`verbose_name_plural` | `applications`
`db_table` | `application`

### Methods

Method | Description
--- | ---
`__str__(self)` | Returns the applicant's username

## Views

