from django.contrib import admin

from .models import WalletRatio
from .models import WalletTokens


@admin.register(WalletTokens)
class WalletTokensAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "date_add_tokens")
    list_filter = ("date_add_tokens",)
    search_fields = ("user__login", "user__nickname", "balance")
    readonly_fields = ("user", "balance", "date_add_tokens")
    fieldsets = (("User Info", {"fields": ("user", "balance", "date_add_tokens")}),)
    ordering = ("-date_add_tokens",)
    verbose_name = "Баланс токенов"
    verbose_name_plural = "Баланс токенов пользователей"


class WalletRatioAdmin(admin.ModelAdmin):
    list_display = ("base_value", "invite_user_bonus")
    list_editable = ("invite_user_bonus",)


admin.site.register(WalletRatio, WalletRatioAdmin)
