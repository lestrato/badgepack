from django.shortcuts import render
import json

from django.contrib.auth.models import User
from rest_framework import viewsets
from api.serializers import *

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, detail_route, authentication_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from django.http import HttpResponse, JsonResponse

from community.fetches import *
from community.models import *
from account.fetches import *
from badge.fetches import *

from api.models import replace_auth_token

def get_user_community_status(community_tag, request):
    community = community_object(community_tag=community_tag)
    if not community:
        return {"error": "Failure - Community not found."}

    membership = u_membership(
        community=community,
        user=request.user,
    )
    if not membership:
        return {"error": "Failure - You are not a member of this community."}

    return {"community": community,
            "user": request.user,
            "user_status": membership.user_status}

def build_community_badge_list(community):
    community_badges = community.get_badge_classes()
    badges = {}

    for b in community_badges:
        badges[b.name] = {
            "name": b.name,
            "description": b.description,
            "created_on": b.created_on,
            "is_available": b.is_available,
            "is_discontinued": b.is_discontinued,
            "earned_by": []
        }

        badge_instances = all_badge_instances(b)
        for i in badge_instances:
            if i.earner not in badges[b.name]["earned_by"]:
                badges[b.name]["earned_by"].append(i.earner.username)

    return badges

def build_community_user_list(community):
    members = {
            "earners": [],
            "moderators": [],
            "owners": []
            }

    community_members = all_community_memberships(community)
    for u in community_members:
        if u.user_status == "owner":
            members["owners"].append(u.user.username)
        elif u.user_status == "moderator":
            members["moderators"].append(u.user.username)
        else:
            members["earners"].append(u.user.username)

    return members

# api/communities/<community_tag>
class APICommunityView(APIView):
    """
    A view that returns community-related info.
    """
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get(self, request, community_tag):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        community = info["community"]

        # If the user is an earner, only return basic community info:
        if info["user_status"] == "earner":
            return Response({
                "name": community.name,
                "description": community.description,
                "tag": community.tag,
                "is_private": community.is_private,
                "created_on": community.created_on
                })
        # If user is an owner or moderator, return 
        else:
            badges = build_community_badge_list(community)
            members = build_community_user_list(community)

            return Response({
                "name": community.name,
                "description": community.description,
                "tag": community.tag,
                "is_private": community.is_private,
                "created_on": community.created_on,
                "members": members,
                "badges": badges,
                })

# api/communities/<community_tag>/users (GET, POST)
class APICommunityUsersView(APIView):
    """
    A view that returns a community's user-related info.
    """
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get(self, request, community_tag):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        if info["user_status"] == "earner":
            return JsonResponse({"error": "Failure - You are not authorized to view this page."}, status=403)

        community = info["community"]
        members = build_community_user_list(community)

        return Response(members)
    
    # Sends an invitation to user(s)
    # POST request should be in format {"users": [list of usernames]}
    def post(self, request, community_tag):    
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        if info["user_status"] == "earner":
            return JsonResponse({"error": "Failure - You are not authorized to view this page."}, status=403)

        json_request = json.loads(request.body.decode("utf-8"))

        if "users" not in json_request:
            return JsonResponse({"error": "Failure - No users specified. Input should be in format {'users': ['user1', 'user2', ...]}"}, status=400)

        community = info["community"]
        users_not_found = ""

        for username in json_request["users"]:
            # Try to find a user with the username:
            target_user = u_instance(username)
            if not target_user:
                users_not_found += "{0}, ".format(username)
            else:
                # Check if the user is already in the community:
                target_membership = u_membership(community, target_user)
                if not target_membership:
                    # Check if the user has an unaccepted application:
                    target_application = u_application(community, target_user)
                    if target_application:
                        target_application = target_application.accept(
                            accepted_by=request.user,
                        )
                        target_application.save()

                        new_membership = Membership(
                            user=target_user,
                            community=community,
                            user_status='earner',
                        )

                        new_membership.save()
                    else:
                        # Check if the user already has an invitation:
                        target_invite = u_invitation(community, target_user)
                        if not target_invite:
                            new_invitation = Invitation(
                                community=community,
                                recipient=target_user,
                                sender=request.user,
                            )
                            new_invitation.save()

        if len(users_not_found) > 0:
            return Response({"message": "Failure - The following users were not found: {0}".format(users_not_found[:-2])})
        else:
            return Response({"success": "Success - Successfully invited users to {0}".format(community_tag)})

# api/communities/<community_tag>/badges (GET, POST)
class APICommunityBadgesView(APIView):
    """
    A view that returns a community's badge-related info.
    """
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get(self, request, community_tag):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        if info["user_status"] == "earner":
            return JsonResponse({"error": "Failure - You are not authorized to view this page."}, status=403)

        community = info["community"]
        badges = build_community_badge_list(community)

        return Response(badges)

    def post(self, request, community_tag):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        if info["user_status"] == "earner":
            return JsonResponse({"error": "Failure - You are not authorized to view this page."}, status=403)

        json_request = json.loads(request.body.decode("utf-8"))

        # Input: {"data": [{"badge": "badge1", "recipients": ["user1", "user2", ...]}, {"badge": "badge2", ...}]}

        if "data" not in json_request:
            return JsonResponse({"error": "Failure - Incorrect input. Format should be {'data': [{'badge': 'badge1_name', 'recipients': ['user1', ...]}, ...]}"}, status=400)

        error_log = {}

        # Go through each badge:
        for val in json_request["data"]:
            if "badge" in val and "recipients" in val:
                badge_name = val["badge"]
                recipients = val["recipients"]

                # Grab the badge instance:
                target_badgeclass = a_badge_class(val["badge"])

                if not target_badgeclass:
                    error_log[badge_name] = ["Failure - No badge with this name exists."]
                    continue

                # Go through each user:
                for u in recipients:
                    # Check if the user exists:
                    target = u_instance(u)
                    if not target:
                        if badge_name in error_log:
                            error_log[badge_name][1].append(u)
                        else:
                            error_log[badge_name] = ["Failure - Could not find the following user(s): ", [u]]
                        continue

                    # Check if the user already has the badge:
                    if not u_badge_instance(target_badgeclass, target):
                        new_instance = BadgeInstance(
                            badge_class=target_badgeclass,
                            earner=target,
                            assigned_by=request.user,
                        )

                        new_instance.save()

                if badge_name not in error_log:
                    error_log[badge_name] = ["Success - Successfully awarded."]

        for k in error_log.keys():
            if len(error_log[k]) == 1:
                error_log[k] = error_log[k][0]
            else:
                tmp = error_log[k][0]
                for x in error_log[k][1]:
                    tmp += "{0}, ".format(x)

                tmp = tmp[:-2]

                error_log[k] = tmp

        return JsonResponse(error_log)

# api/communities/<community_tag>/leaderboard (GET)
class APILeaderboardView(APIView):
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get(self, request, community_tag):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        earner_list = all_earners(
            community=info["community"],
        )

        tmp = {}

        for earner in earner_list:
            u_badges = u_badge_count(
                earner=earner.user, 
                community=info["community"]
            )
            if u_badges in tmp:
                # NTS: append the user's anon. ID instead
                tmp[u_badges].append(earner.user)
            else:
                # NTS: append the user's anon. ID instead
                tmp[u_badges] = [earner.user]

        counts = tmp.keys()
        counts.sort(reverse=True)

        curr_rank = 1
        full_leaderboard = []

        for x in counts:
            full_leaderboard.append([curr_rank, x, tmp[x]])
            curr_rank += len(tmp[x])

        if info["user_status"] == 'earner':
            # Find user's placement in the leaderboard:
            for x in range(0, len(full_leaderboard)):
                if info["user"] in full_leaderboard[x][2]:
                    # Keep track of user's placement:
                    user_rank = full_leaderboard[x][0]
                    break

            if len(full_leaderboard) < 5:
                leaderboard = full_leaderboard
            else:
                start_range = x - 2
                end_range = x + 3

                while start_range < 0:
                    start_range += 1
                    end_range += 1

                while end_range > len(full_leaderboard):
                    end_range -= 1
                    start_range -= 1

                leaderboard = full_leaderboard[start_range:end_range]
        else:
            leaderboard = full_leaderboard[:]

        retval = []

        for i in range(0, len(leaderboard)):
            user_list = []

            for u in leaderboard[i][2]:
                profile = u_profile_by_user(u)
                user_list.append(profile.public_id)

            user_ids = ", ".join(x for x in user_list)
            retval.append({"rank": leaderboard[i][0], "badges": leaderboard[i][1], "users": user_ids})

        return JsonResponse({"leaderboard": retval})

# api/communities/<community_tag>/badges/<user_id>
class APISingleUserBadgeView(APIView):
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get(self, request, community_tag, user_id):
        info = get_user_community_status(community_tag, request)

        if "error" in info:
            return JsonResponse({"error": info["error"]}, status=404)

        if info["user_status"] == "earner":
            return JsonResponse({"error": "Failure - You are not authorized to view this page."}, status=403)

        # Check if target user exists:
        target = u_instance(user_id)
        if not target:
            return JsonResponse({"error": "Failure - This user does not exist."}, status=404)

        # Check if target is part of the community:
        target_membership = u_membership(info["community"], target)
        if not target_membership:
            return JsonResponse({"error": "Failure - This user is not a member of {0}".format(community_tag)}, status=404)

        # Get the user's badges:
        target_badges = u_community_badge_instances(target, info["community"])
        res = ", ".join(x.badge_class.name for x in target_badges if len(target_badges) != 0)

        return Response({"success": res})

class APIReplaceTokenView(APIView):
    renderer_classes = (JSONRenderer, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def post(self, request):
        tkn = replace_auth_token(user=request.user)
        if tkn:
            return JsonResponse({"token": str(tkn)})
        else:
            return JsonResponse({"error": "Token could not be updated."})

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'communities': reverse('community-list', request=request, format=format)
    })