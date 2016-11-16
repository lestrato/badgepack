## What is the difference between a "public" and "private" community?
**Public** communities can be joined by any user, so long as they have a link to the community page.

![](images/public_community.png)

**Private** communities require users to send in an application to join the community. Community moderators must then approve the request before the user can join.

![](images/private_community.png)

## How do I add a new community?
At the moment, new communities can only be created through the admin panel (`/admin`). Here are the steps to do so:

1. Click on "Add" next to "Communities" under the "Community" section.
2. Enter details related to the community:
    * `Name` The name of your community (max. 20 characters).
    * `Description` A brief description of what the community is for/about. This will be displayed under the "About Community" section of the community page, and is editable by community moderators under the "Community Settings" page.
    * `Tag` A short identifier for your community (max. 10 characters). The "tag" is what the community will be listed as under the navigation bar, as well as on the "My Badges" page. An example of a good tag would be the course code, if this is a community for a course.
    * `Is private` If checked, the community will be marked as private.
3. Press "SAVE".

You will likely want to assign at least one member as the community's first moderator: 

1. Click on `Add` next to `Memberships` under the `Community` section. 
2. Select the user you'd like to set as a moderator, and the name of community you want to add a moderator to. 
3. Check the `Is moderator` box.
4. Press `SAVE`.

## How do I join a community?
You can join a community through any of the following:
* Accepting a community invitation from a moderator
* Visiting a public community page and clicking `Join Community`
* Visiting a private community page, clicking `Apply to Join`, and then having your application accepted by a community moderator

## How do I add users to my community?

You can either share the link to the community with users and have them join / send an application, or send out community invitations.

To send a community invitation:

1. Go to the community's page.
2. Click on `Manage Users` -> `Invites` -> `Invite a User`
3. Enter the username of the user you'd like to invite.
4. Click `Invite users`

Users will then be able to view their invitations and accept them, which will then add them to the community.

## I am a community moderator. How do I set other community members as moderators for my community?

1. Go to the community's page.
2. Click on `Manage Users` -> `Members`
3. Find the user you want to set as a moderator, and click on the cog icon under the `Actions` column.
4. In the dropdown menu for `Permissions`, select `moderator`
5. Click `Save`

## How do I make a badge?
Badges can only be created by community moderators of a community.

1. Go to the community's page.
2. Under `Manage Badges`, click on the `Create a new badge` button.
3. Fill out _all_ fields in the pop-up window.
4. Click `Add Badge`.

Note that newly-created badges are initially set to be "unavailable". Unavailable badges cannot be seen by non-moderators, and cannot be gifted/assigned to anyone until made available. 

The following table outlines which actions are available, given the state of the badge:

Action | Unavailable | Available
--- | --- | ---
Edit | O | X
Make Available | O | X
Assign | X | O
Delete | O | O

Note that you cannot edit a badge once it has been made available.

## How do I give badges to users?

There are two ways of gifting badges to users.

### Assigning one badge to multiple users

1. Go to the community's page.
2. Hover over the badge you'd like to assign.
3. Click on `Assign`.
4. Check the `Gift` checkbox for every user you'd like to give the badge to.
5. Click `Gift Badge`

### Assigning multiple badges to one user

1. Go to the community's page.
2. Click on `Manage Users` -> `Members`
3. Find the user you want to set as a moderator, and click on the cog icon under the `Actions` column.
4. For each badge you'd like to assign to the user, set `Actions` to `Gift`.
5. Click `Confirm`.

## How do I revoke a badge?
Badges cannot be revoked.