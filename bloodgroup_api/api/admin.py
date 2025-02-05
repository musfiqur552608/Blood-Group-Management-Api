from django.contrib import admin
from .models import BloodGroup, UserProfile


@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'area', 'phone')
    list_filter = ('user__username', 'blood_group__name', 'area', 'phone')
    search_fields = ('user__username', 'blood_group__name', 'area', 'phone')
