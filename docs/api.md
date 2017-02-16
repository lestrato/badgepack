# API

# Quick Reference

* [Get user authorization token](#obtaining-your-authorization-token)
* [Reset authorization token](#replacing-your-authorization-token)
* [Get community info](#get-apicommunitiescommunity_tag62)
* [Get community user list](#get-apicommunitiescommunity_tag62users)
* [Batch invite users to a community](#post-apicommunitiescommunity_tag62users)
* [Get community badge list](#get-apicommunitiescommunity_tag62badges)
* [Batch gift badges in a community](#post-apicommunitiescommunity_tag62badges)
* [Get single user's badge list within a community](#get-apicommunitiescommunity_tag62badgesusername62)
* [Get community leaderboard info](#get-apicommunitiescommunity_tag62leaderboard)

# Authorization Token
Requests to the following URLs require you to pass in an authorization token in the header, like so:
```
curl -H "Authorization: Token 83ef520b64f58ee33e537d821e6b73a90ac6d1f7" <url>
```

## Obtaining Your Authorization Token
Users may obtain their authorization token by making a POST request to `api/auth-token/` with their username and password, like so:
```
curl -X POST --form username=my_username --form password=my_password http://127.0.0.1:8000/api/auth-token/
```

If proper credentials were supplied, the following is returned:
`{"token": user's auth token}`

Tokens do not expire, but may be replaced (see below).

## Replacing Your Authorization Token
Users may replace their authorization token by making a POST request to `api/replace-token/`. The header must include their current authorization token, like so:
```
curl -H "Authorization: Token 83ef520b64f58ee33e537d821e6b73a90ac6d1f7" -X POST http://127.0.0.1:8000/api/replace-token/
```

If the operation was successful, the following is returned:
```{"token": user's new token}```

If the operation failed, the following is returned:
```{"error": "Token could not be updated."}```

When a new token is generated, it will overwrite the previous one, thus deactivating the older token.

# [GET] api/communities/<community_tag\>
### Description
Returns information about a community. The amount of information returned depends on the requester's community status (earner, moderator, owner).

### Requirements
* Token must be passed in via header.
* Requester must be a member of `<community_tag>`

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is an earner in the community:
```
{
    "name": community's name,
    "description": community's description,
    "tag": community's tag (e.g. CSC108),
    "is_private": true/false,
    "created_on": timestamp of when the community was created
}
```

If the requester is a moderator or owner of the community:
```
{
    "name": community's name,
    "description": community's description,
    "tag": community's tag (e.g. CSC108),
    "is_private": true/false,
    "created_on": timestamp of when the community was created,
    "members": collection of community members (refer to sample),
    "badges": collection of badges in the community (refer to sample)
}
```

### Sample Usage

Input
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" http://127.0.0.1:8000/api/communities/Test2
```

Output
```
{
    "name":"Alt. Test Community",
    "created_on":"2017-01-12",
    "tag":"Test2",
    "is_private":true,
    "description":"!",
    "badges":
        {
            "Badge 4":
                {
                    "is_discontinued":false,
                    "description":"Placeholder description.",
                    "earned_by":[],
                    "created_on":"2017-01-12",
                    "is_available":true,
                    "name":"Badge 4"
                },
            "Badge 1":
                {
                    "is_discontinued":false,
                    "description":"Placeholder description.",
                    "earned_by":["user1"],
                    "created_on":"2017-01-12",
                    "is_available":true,
                    "name":"Badge 1"
                }
        },
    "members":
        {
            "earners":["user1","user2","user3"],
            "moderators":[],
            "owners":["owner1]
        }
}
```

# [GET] api/communities/<community_tag\>/users
### Description
Returns information about a community's members.

### Requirements
* Token must be passed in via header.
* Requester must be an owner or moderator of the community.

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is not an owner or moderator of the community:
```
{"error": "Failure - You are not authorized to view this page."}
```
Success:
```
{
    "earners": list of usernames,
    "moderators": list of usernames,
    "owners": list of usernames
}
```

### Sample Usage

Input:
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" http://127.0.0.1:8000/api/communities/Test2/users
```

Output:
```
{
    "earners":["user1","user2","user3"],
    "moderators":[],
    "owners":["owner1"]
}
```

# [POST] api/communities/<community_tag\>/users
### Description
Given a list of usernames, sends out a community invitation to each mentioned username.

### Requirements
* Token must be passed in via header.
* Requester must be an owner or moderator of the community.

### Request Body
```
{
    "users": [list of usernames]
}
```

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is not a moderator or owner:
```
{"error": "Failure - You are not authorized to view this page."}
```

If the body is empty or does not contain a list of users:
```
{"error": "Failure - No users specified. Input should be in format {'users': ['user1', 'user2', ...]}"}
```

If at least one username in the user list is invalid (note that invitations will still be sent out to valid users):
```
{"message": "Failure - The following users were not found: user1, user2, ..."}
```

If all users were successfully invited:
```
{"success": "Success - Successfully invited users to <community_tag>"}
```

### Sample Usage
Input:
```
{curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" -X POST -d '{"users":["user1", "user2", "user3", "user4"]}' http://127.0.0.1:8000/api/communities/Test3/users
```

Output:
```
{"success":"Success - Successfully invited users to Test3"}>
```

# [GET] api/communities/<community_tag\>)/badges
### Description
Returns information about a community's badges.

### Requirements
* Token must be passed in via header.
* Requester must be an owner or moderator of the community.

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is not a moderator or owner:
```
{"error": "Failure - You are not authorized to view this page."}
```

Success:
```
{
    "badge1_name":
        {
            "is_discontinued": true/false,
            "description": community description,
            "earned_by": list of usernames,
            "created_on": timestamp,
            "is_available": true/false,
            "name": badge1_name
        },
    "badge2_name": {...},
    ...
}
```

### Sample Usage
Input:
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" http://127.0.0.1:8000/api/communities/Test2/badges
```

Output:
```
{
    "Badge 3":
        {
            "is_discontinued":false,
            "description":"Placeholder description.",
            "earned_by":[],
            "created_on":"2017-01-12",
            "is_available":true,
            "name":"Badge 3"
        },
    "Badge 2":
        {
            "is_discontinued":false,
            "description":"Placeholder description.",
            "earned_by":["user1","user2"],
            "created_on":"2017-01-12",
            "is_available":true,
            "name":"Badge 2"
        },
    "Badge 1":
        {
            "is_discontinued":false,
            "description":"Placeholder description.",
            "earned_by":["user1"],
            "created_on":"2017-01-12",
            "is_available":true,"name":"Badge 1"
        }
}
```
# [POST] api/communities/<community_tag\>)/badges
### Description
Given a mapping of username list to badge names, awards badges to users within a community.

### Requirements
* Token must be passed in via header.
* Requester must be an owner or moderator of the community.

### Request Body
```
{
    "data":
        [
            {
                "badge": badge1_name,
                "recipients": list of usernames
            },
            ...
        ]
}
```

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is not a moderator or owner:
```
{"error": "Failure - You are not authorized to view this page."}
```

Success and failure messages are returned for each badge, like so:
```
{
    "badge1_name": "Success - Successfully awarded.",
    "badge2_name": "Failure - Could not find the following user(s): user1, user2, ...",
    "invalid_badge": "Failure - No badge with this name exists."
    ...
}
```

### Sample Usage
Input:
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" -X POST -d 
'{"data":
    [{
        "badge": "Text Badge", 
        "recipients": ["user1", "user2"]
    }, 
    {
        "badge": "Methodology Badge", 
        "recipients": ["user1", "abcabc"]
    }, 
    {
        "badge": "Fake Badge", 
        "recipients": []
    }]
}' http://127.0.0.1:8000/api/communities/Test/badges
```

Output:
```
{
    "Text Badge": "Success - Successfully awarded.", 
    "Fake Badge": "Failure - No badge with this name exists.", 
    "Methodology Badge": "Failure - Could not find the following user(s): abcabc"
}
```

# [GET] api/communities/<community_tag\>/badges/<username\>
### Description
Returns a list of badges earned in `<community_tag>` by `<username>`.

### Requirements
* Token must be passed in via header.
* Requester must be an owner or moderator of the community.

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

If the requester is not a moderator or owner:
```
{"error": "Failure - You are not authorized to view this page."}
```

If `<username>` does not exist:
```
{"error": "Failure - This user does not exist."}
```

If `<username>` is not a member of `<community_tag>`:
```
{"error": "Failure - This user is not a member of <community_tag>"}
```

Success:
```
{"success": comma-separated list of badge names}
```

### Sample Usage
Input:
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" http://127.0.0.1:8000/api/communities/Test2/badges/user1
```

Output:
```
{
    "success":"Badge 1, Badge 2"
}
```

# [GET] api/communities/<community_tag\>/leaderboard
### Description
Returns leaderboard / ranking information for a community (public IDs only). If the requester is an owner or moderator of the community, the entire leaderboard will be returned. Else, a subset will be returned.

The subset contains (at most) five ranks close to (and including) the requester's rank.

### Requirements
* Token must be passed in via header.
* Requester must be a member of the community.

### Return Value
If the community does not exist:
```
{"error": "Failure - Community not found."}
```

If the requester is not a member of the community:
```
{"error": "Failure - You are not a member of this community."}
```

Success:
```
{"leaderboard": list of collections with badge counts, rank, and public IDs (see below)}
```

### Sample Usage
Input:
```
curl -H "Authorization: Token e6969012c16d6ba79fc04932320a44ece6ef7e27" http://127.0.0.1:8000/api/communities/Test/leaderboard
```

Output:
```
{
    "leaderboard": 
        [
            {
                "badges": 8, 
                "rank": 1, 
                "users": "Mango"
            }, 
            {
                "badges": 7, 
                "rank": 2, 
                "users": "Anonymous Blackberry"
            }, 
            {
                "badges": 5, 
                "rank": 3, 
                "users": "Anonymous Persimmon, Pineapple, Anonymous Mango, Anonymous Melon, Anonymous Raisin, Anonymous Guava"
            }
        ]
}
```