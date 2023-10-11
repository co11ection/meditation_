from rest_framework import serializers
from wallet.models import WalletTokens


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTokens
        fields = "__all__"
