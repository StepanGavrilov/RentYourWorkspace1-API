from rest_framework import serializers, status

from django.db.models import Q

from account_system_api.serializers import AccountSerializer
from rest_framework.relations import RelatedField

from .models import Reservation, Office


class OfficeSerializer(serializers.ModelSerializer):
    """
    Оффис общий сериализатор
    """

    class Meta:
        model = Office
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        office = Office.objects.create(**validated_data)
        return office


class OfficeReservationSerializer(serializers.ModelSerializer):
    """
    Оффис + Брони
    """

    datetime_from = serializers.DateTimeField(required=False)
    datetime_to = serializers.DateTimeField(required=False)

    class Meta:
        model = Office
        fields = ('id', 'name', 'description', 'datetime_from', 'datetime_to')


class OfficeUpdateSerializer(serializers.ModelSerializer):
    """
    Обновление информации о оффисе
    """

    name = serializers.CharField(max_length=32, required=False)
    description = serializers.CharField(max_length=512, required=False)

    class Meta:
        model = Office
        fields = ('id', 'name', 'description')

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ReservationSerializer(serializers.ModelSerializer):
    """
    Полная информация о брони

    customer -> django.setting.AUTH_USER_MODEL
    """

    customer = AccountSerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'office', 'datetime_from', 'datetime_to')
        depth = 1


class ReservationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Создаём / Обновляем бронь
    """

    office = serializers.IntegerField(source='office_id')

    class Meta:
        model = Reservation
        fields = ('id', 'office', 'datetime_from', 'datetime_to')

    def create(self, validated_data):
        """
        Создания брони состоит из проверки 3 уровней

        office_id -> офис, где хотим арендовать помещение
        level1 -> Проверяем rangeОм (Начало, Конец) - включающий
        start_rent -> Начало аренды (Может равнятся концу аренды другого человека)
        end_rent -> Конец аренды
        """

        start_rent = validated_data['datetime_from']
        end_rent = validated_data['datetime_to']
        office_id = validated_data['office_id']

        if end_rent < start_rent:
            raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)

        level_1 = Reservation.objects.select_related().filter(
            Q(datetime_from__range=(start_rent, end_rent)) | Q(datetime_to__range=(end_rent, end_rent)),
            office=office_id)

        check = (level_1.exists())

        if not check:
            """
            Если нет аренды
            """
            reservation = Reservation.objects.create(**validated_data)
            return reservation
        raise serializers.ValidationError(code=status.HTTP_400_BAD_REQUEST)

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
