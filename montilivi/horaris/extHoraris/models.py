# This Python file uses the following encoding: utf-8

from django.db import models
from django.db.models import Manager, QuerySet

class Grup(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    fusio = models.BooleanField()
    nomFusio = models.CharField(max_length=50, blank=True)
    codiXtec = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.nom)

    @staticmethod
    def objectes():
        #type: ()->QuerySet
        return Grup.objects

    class Meta:
        ordering = ['nom']

class Materia(models.Model):
    codi = models.CharField(max_length=15)

    def __unicode__(self):
        return unicode(self.codi)

class Profe(models.Model):
    nomUsuari = models.CharField(max_length=50)
    nomComplert = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.nomUsuari)

class Franja(models.Model):
    descripcio = models.CharField(max_length=25)

    def __unicode__(self):
        return unicode(self.descripcio)

class Dia(models.Model):
    nom = models.CharField(max_length=15)

    def __unicode__(self):
        return unicode(self.nom)

class Aula(models.Model):
    nom = models.CharField(max_length=15)

    def __unicode__(self):
        return unicode(self.nom)

class EntradaHorari (models.Model):
    materia = models.ForeignKey('extHoraris.materia',  db_index=True)
    profe = models.ForeignKey('extHoraris.profe',  db_index=True, on_delete=models.PROTECT)
    grup = models.ForeignKey('extHoraris.grup', db_index=True)
    aula = models.ForeignKey('extHoraris.aula', db_index=True)
    dia = models.ForeignKey('extHoraris.dia', db_index=True)
    franja = models.ForeignKey('extHoraris.franja', db_index=True)

    class Meta:
        verbose_name = u'Entrada de l\'horari'
        unique_together = ("materia", "profe", "grup", "aula", "dia", "franja")

    def __unicode__(self):
        return unicode(self.materia) + u' -> '+ unicode(self.aula)

    @staticmethod
    def objectes():
        #type: ()->QuerySet
        return EntradaHorari.objects
