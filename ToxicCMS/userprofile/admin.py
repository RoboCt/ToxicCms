from django.contrib import admin
from userprofile.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Profile, ProfileAdmin)
