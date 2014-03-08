from django.contrib import messages
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from aula.apps.incidencies.models import Incidencia


class extSMS(models.Model):
    text = models.CharField(max_length=160)



@receiver(post_save, sender=Incidencia)
def my_handler(sender, instance, **kwargs):
    print instance.alumne

@receiver(post_delete, sender=Incidencia)
def paco(sender, **kwargs):
    print "PACO"

