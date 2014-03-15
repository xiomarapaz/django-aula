from django.contrib import messages
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from aula.apps.presencia.models import ControlAssistencia


OPCIONS = (
    ('enviar','enviar'),
    ('anular','anular'),
    ('res','res')
)

class extSMS(models.Model):
    falta = models.ForeignKey(ControlAssistencia)
    estat = models.CharField(max_length=20, choices=OPCIONS)



