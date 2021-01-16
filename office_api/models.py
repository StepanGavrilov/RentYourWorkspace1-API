from django.db import models
from django.conf import settings


class Office(models.Model):

    name = models.CharField(
        max_length=32,
        verbose_name='Office'
    )
    description = models.CharField(
        max_length=512,
        verbose_name='Office'
    )

    class Meta:
        verbose_name = 'Office'
        verbose_name_plural = 'Offices'

    def __str__(self):
        return f'Office name: {self.name} Id: {self.id}'


class Reservation(models.Model):

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Customer'
    )

    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name='reservation',
        verbose_name='Office'
    )

    datetime_from = models.DateTimeField(
        db_index=True,
        verbose_name='Start rent'
    )

    datetime_to = models.DateTimeField(
        db_index=True,
        verbose_name='End rent'
    )

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'Id: {id} Reservation for: {self.customer}'