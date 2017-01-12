from django.contrib import admin
from account.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('profile_id',) #'created', 'name',
    list_display = ('user', 'public_id', 'profile_id',)
    list_filter = ()
    search_fields = ('user', 'public_id', 'profile_id',)
    fieldsets = (
        ('Properties', {'fields': ('user', 'profile_id', 'public_id',)}),
    )
    pass

admin.site.register(Profile, ProfileAdmin)