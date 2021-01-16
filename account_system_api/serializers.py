from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для Аккаунта
    """

    class Meta:
        model = Account
        fields = ('id', 'username', 'email')


class AccountUpdateSerializer(serializers.ModelSerializer):
    """
    Create serializer
    """

    username = serializers.CharField(max_length=32, required=False)
    email = serializers.EmailField(max_length=64, required=False)

    class Meta:
        model = Account
        fields = ('username', 'email')

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AccountCreateSerializer(serializers.ModelSerializer):
    """
     Update serializer
     """

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data) -> Account:
        account = Account.objects.create_user(**validated_data)
        return account

