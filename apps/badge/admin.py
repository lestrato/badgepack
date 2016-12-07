from django.contrib import admin
from badge.models import BadgeClass, BadgeInstance

class BadgeClassAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('name', 'description', 'slug', 'image', 'community', 'earnable_by', 'creator',
        'created_on', 'is_available', 'is_discontinued',)
    list_filter = ('is_available', 'is_discontinued',)
    search_fields = ('name', 'description', 'community', 'creator', 'earnable_by',)
    fieldsets = (
        ('Metadata', {'fields': ('creator', 'created_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('name', 'description', 'community', 'image',)}),
        ('Access', {'fields': ('earnable_by', 'is_available', 'is_discontinued',)}),
    )
    pass

admin.site.register(BadgeClass, BadgeClassAdmin)

class BadgeInstanceAdmin(admin.ModelAdmin):
    readonly_fields = () #'created', 'name',
    list_display = ('earner', 'badge_class', 'recieved_on', 'assigned_by',)
    list_filter = ()
    search_fields = ('earner', 'badge_class', 'assigned_by')
    fieldsets = (
        ('Metadata', {'fields': ('recieved_on',)}),#', classes': ('collapse',)
        ('Properties', {'fields': ('earner', 'badge_class', 'assigned_by',)}),
    )
    pass

admin.site.register(BadgeInstance, BadgeInstanceAdmin)
