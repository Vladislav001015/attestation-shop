from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _

from accounts.models import CustomUser


class Order(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(_('Имя'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    address = models.CharField(_('Адрес'), max_length=100)
    receiver_number = PhoneNumberField(_('Номер телефона получателя'), blank=True, null=True)
    date_delivery = models.DateField(_('Дата доставки'))
    comment = models.CharField(_('Комментарий'), max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

