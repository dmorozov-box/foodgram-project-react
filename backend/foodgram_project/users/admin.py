from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Subscription

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name'
    )
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
