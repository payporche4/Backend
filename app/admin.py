from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import Dashboard, TransactionRecord, Service, Category, MetaTags


class TransactionRecordAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount", "timestamp")
    search_fields = ("sender", "amount", "receiever")
    readonly_fields = ("sender", "receiver", "amount")


admin.site.register(TransactionRecord, TransactionRecordAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "price", "description")
    search_fields = ("owner",)
    # readonly_fields = ('id', 'owner', 'price', 'thumbnail', 'description')


admin.site.register(Service, ServiceAdmin)


class DashboardAdmin(admin.ModelAdmin):
    list_display = ("user", "wallet_tag", "wallet_balance")
    search_fields = ("user",)
    readonly_fields = ("user", "wallet_balance", "wallet_tag")


admin.site.register(Dashboard, DashboardAdmin)


class MetaTagsAdmin(admin.ModelAdmin):
    list_display = ("metatag", "timestamp")
    search_fields = ("metatag",)
    readonly_fields = ("timestamp",)


admin.site.register(MetaTags, MetaTagsAdmin)

admin.site.register(Category)
