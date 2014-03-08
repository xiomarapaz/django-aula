from django.contrib import messages
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from aula.apps.incidencies.models import Incidencia


class extSMS(models.Model):
    incidencia = models.ForeignKey(Incidencia)
    envia = models.BooleanField(default=False)


@receiver(post_save, sender=Incidencia)
def crea_sms(sender, instance, **kwargs):
    extSMS.objects.create(incidencia=instance)

@receiver(pre_delete, sender=Incidencia)
def borra_sms(sender, instance, **kwargs):
    try:
        extSMS.objects.get(incidencia=instance).delete()
    except extSMS.DoesNotExist:
        pass




