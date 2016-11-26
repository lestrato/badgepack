from django.contrib import admin
from community.models import Community, Membership, Invitation, Application

class CommunityAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('name', 'description', 'tag', 'created_on', 'is_private',)
    list_filter = ('is_private',)
    search_fields = ('name', 'tag',)
    fieldsets = (
        ('Metadata', {'fields': ('created_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('name', 'description', 'tag',)}),
        ('Access', {'fields': ('is_private',)}),
    )
    pass

admin.site.register(Community, CommunityAdmin)

class MembershipAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('user', 'community', 'joined_on', 'user_status')
    list_filter = ('user_status',)
    search_fields = ('user', 'community',)
    fieldsets = (
        ('Metadata', {'fields': ('joined_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('user', 'community')}),
        ('Permissions', {'fields': ('user_status',)}),
    )
    pass

admin.site.register(Membership, MembershipAdmin)

class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('recipient', 'community', 'created_on', 'sender', 'to_be_moderator')
    list_filter = ('to_be_moderator',)
    search_fields = ('sender', 'community', 'recipient')
    fieldsets = (
        ('Metadata', {'fields': ('created_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('sender', 'community', 'recipient',)}),
        ('Permissions', {'fields': ('to_be_moderator',)}),
    )
    pass

admin.site.register(Invitation, InvitationAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('applicant', 'community', 'created_on',  'accepted_by')
    list_filter = ()
    search_fields = ('applicant', 'community', 'accepted_by')
    fieldsets = (
        ('Metadata', {'fields': ('created_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('applicant', 'community', 'accepted_by')}),
    )
    pass

admin.site.register(Application, ApplicationAdmin)
