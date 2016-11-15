# Script

## Introduction

Hi <user>, I'm <name> and I'm hoping to gather user feedback on Badgepack, a web-based badge achievement system. I'll be asking you to go through a few tasks, and for each task, I ask that you voice your thoughts as often as possible.

(open the website)

## Tasks

### Moderator

* First, we will be going through the site as a moderator. Please login with the username "admin" and the password "monday123". Both of these are in lowercase.
* We want to go to the community page for the course "ABC123". How do you think we can get to it?
* Please add a new badge to ABC123 with any name, description, and image you'd like.
* Now, let's move onto some user management stuff. If you wanted to view a list of users in the community, how would you do so?
* "potato" has a really good username, so let's award them for it. How would you give "potato" the badge you just created?
* Okay, now let's say you want to add a new user to the community, and their username is "user". How would you do it?
* Someone has informed you that the description for the community has a typo. How do you think we could fix it?
* _(on the Community Settings page)_ This is where you would find and modify settings for a community. What do you think about this page? Is it straightforward and intuitive to use? Do you feel like it might benefit from more stuff?
    * If "yes": ask them to elaborate.
* A community can be set to either public or private. What do you think this means?
* A user has sent in an application to join the ABC123 community. How would you view and accept their request?
* "potato" wants to be a moderator for ABC123. How would you change their permissions?
* Some users are feeling badge-deprived. Say you want to give a badge to every user in the community. How would you do so?
* In this short span of time, "potato" has been abusing their powers. Change their permissions back to that of a regular user.
* Do you have any further thoughts about the site when viewing it as a moderator of various communities? Feel free to click around and explore the site.


### User

* Now we're going to go through the site as a regular user. Please log out of the site, and sign in with the username "user", and password "monday123".
* This is what users see for the first time when joining the site. At the moment, you're not a part of any community, so let's go ahead and join one. Earlier, we sent an invitation to ABC123 to this user. How would you view and accept the invitation?
* Your main page has now been updated to show the badges in the community. Since we only created one badge earlier, there is only one badge listed in the community. How do you feel about the way this page currently looks?
* Navigate to the community page for ABC123. This is what a community page looks like for a regular user of a community. What do you think about it, layout and content-wise?
    * Is there anything else you'd like to see on this page?
* Finally, log out and sign in as the user "potato", using the password "monday123". "potato" is a member of multiple communities, and their main page displays a list of all their communities, as well as which badges they've earned.
    * How do you feel about this layout?
* Feel free to click around and explore the site as "potato". Do you have any further thoughts about the site when viewing it as a regular user?

# Notes

## User Stories

### User
* log into the system
* search for a community
* request to join a community
* accept an invitation to join a community
* <del>leave a community</del>
* view all earned badges in my backpack
* view all unearned/earned badges in a community
* view my progress towards earning a badge

### Moderator
* set another user as a moderator to this community
* accept a user's request to join my community
* invite a user to join my community
* remove moderator privileges from a moderator in my community
* create a badge for my community
* discontinue a badge for my community
* <del>set a badge to be available/unavailable to achieve in my community</del>
* assign a badge to users inside of my community

### Admin
* set another user as an admin
* create a community
* discontinue a community
* set a user as a moderator to this community

## Questions / Comments

* We have the functionality for users to join communities, but there is no way of searching for communities to join at the moment.

* Moderators: add a way to see a list of which users have received which badge, and a way to export this information as a CSV? (`name,badge1_name,badge2_name,...`)

* When doing user testing: if I demo to an instructor, should I ask them to go through both the moderator and earner views of the site?
    * How about if I demo to a student?    

## Things to Add

* Resources to help people know how to do things
* Visual feedback when you earned a badge?