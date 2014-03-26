from django.contrib import messages
from django.db import models

# Create your models here.
from aula.apps.alumnes.models import Alumne
from aula.apps.presencia.models import Impartir

OPCIONS = (
    ('enviar','enviar'),
    ('anular','anular'),
    ('res','res')
)

class extSMS(models.Model):
    Alumne = models.ForeignKey(Alumne)
    Dia = models.DateField(db_index=True)
    faltes = models.IntegerField(default=1)
    estat = models.CharField(max_length=20, choices=OPCIONS, default='res')
    intents = models.IntegerField(default=0)
    enviat = models.BooleanField(default=False)



