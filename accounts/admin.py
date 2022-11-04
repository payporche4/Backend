from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile


class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "username")
    readonly_fields = ("id", "date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Resource: http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
