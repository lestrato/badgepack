from django.contrib import admin
from community.models import Community, Membership

class CommunityAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('name', 'description', 'tag', 'created_on', 'is_private',)
    list_filter = ('tag', 'created_on', 'is_private',)
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
    list_display = ('user', 'community', 'joined_on', 'is_moderator')
    list_filter = ('is_moderator', 'joined_on',)
    search_fields = ('user', 'community',)
    fieldsets = (
        ('Metadata', {'fields': ('joined_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('user', 'community')}),
        ('Permissions', {'fields': ('is_moderator',)}),
    )
    pass

admin.site.register(Membership, MembershipAdmin)
