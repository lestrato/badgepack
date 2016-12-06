# Backend
    work
    ├── apps
    │   ├── community

## admin.py
* CommunityAdmin
* MembershipAdmin
* InvitationAdmin
* ApplicationAdmin

## fetches.py
Name | Description
--- | ---
`community_object(community_tag)` | **Returns**: community object with the tag `community_tag`
`all_community_applications(community):` | **Returns**: all application objects for the community `community`
`u_application(community, user)` | **Returns**: an application object for the user `user` and the community `community`, or None if it doesn't exist
`all_community_memberships(community)` | **Returns**: all membership objects for the community `community`
`u_membership(community, user)` | **Returns**: a membership object for the user `user` and the community `community`, or None if it doesn't exist
`u_invitation(community, user)` | **Returns**: a invitation object for the user `user` and the community `community`, or None if it doesn't exist
`all_community_invitations(community)` | **Returns**: all invitation objects for the community `community`
`u_communities(members, user_status=None)` | **Returns**: all community objects with the member `members` and the membership user status `user_status`, or all communities if `user_status` is not specified

## forms.py
Name | Description
--- | ---
`UserPermissionForm` | **Fields**: permissions<br>**Functions**: none
`UserSearchForm` | **Fields**: username<br>**Functions**: clean_username(self)
`CSVUploadForm` | **Fields**: csv_file<br>**Functions**: clean_csv_file(self)
`CommunityPrivacyForm` | **Fields**: privacy<br>**Functions**: none
`CommunityDescriptionForm` | **Fields**: description<br>**Functions**: none

## models.py
### Community

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

### Membership

Name | Field | Settings | Description
--- | --- | --- | ---
`user` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE` | A user who is a member of the community
`community` | `ForeignKey` | `Community`<br/>`on_delete=models.CASCADE` | The community that the user is a member of
`joined_on` | `DateField` | `default=datetime.now` | Date and time the user joined the community
`user_status` | `ChoiceField` | `default=earner` | The community user-type : earner, moderator, or owner

### AbstractRequest

Name | Field | Settings | Description
--- | --- | --- | ---
`community` | `ForeignKey` | `Community`<br/>`on_delete=models.CASCADE`<br/> | The community involved in the request
`created_on` | `DateField` | `default=datetime.now` | The date and time that the request was made

### Invitation

Name | Field | Settings | Description
--- | --- | --- | ---
`recipient` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='invitation_recipient'` | The user who received the invitation
`sender` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='invitation_sender'` | The moderator who sent the invitation

### Application

Name | Field | Settings | Description
--- | --- | --- | ---
`accepted_by` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='application_accepted_by'` | The moderator who accepted the application
`applicant` | `ForeignKey` | `settings.AUTH_USER_MODEL`<br/>`on_delete=models.CASCADE`<br/>`related_name='application_applicant'` | The user who submitted the application

## tests.py
There doesn't seem to be anything here.

## views.py
There doesn't seem to be anything here.

---
# Frontend

    work
    ├── static
    │   ├── templates
    │   |   ├── community

## templates
Name | Description
--- | ---
`community.html` | Base template for all community pages
`components/about_tab.html` | About tab component for the community page
`components/badge_tab.html` | Badges tab component for the community page
`components/members_tab.html` | Members tab component for the community page
`components/nav_pills.html` | The nav-pills component for navigating through the three tabs
