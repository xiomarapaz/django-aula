# This Python file uses the following encoding: utf-8
from aula.apps.assignatures.abstract_models import AbstractTipusDAssignatura,\
    AbstractAssignatura
from aula.apps.assignatures.business_rules.assignatura import \
    assignatura_post_save, assignatura_clean, assignatura_pre_save
from django.db import models
from aula.apps.alumnes.models import Alumne
from django.core.exceptions import ValidationError

class TipusDAssignatura(AbstractTipusDAssignatura):
    pass

class Assignatura(AbstractAssignatura):
    def clean(self):
        assignatura_clean(self)

# ----------------------------- B U S I N E S S       R U L E S ------------------------------------ #
from django.db.models.signals import post_save, pre_save, pre_delete

#Assignatura
pre_save.connect(assignatura_pre_save, sender = Assignatura )
post_save.connect(assignatura_post_save, sender = Assignatura )

#-----------------------------------------------------------------------

class UF(models.Model):
    nom = models.CharField(max_length=25)
    dinici = models.DateTimeField()
    dfi = models.DateTimeField()
    horesTeoriques = models.IntegerField()
    assignatura = models.ForeignKey(Assignatura, null=False, blank=False)

    def clean(self):
        #Validació de les dades del model.
        if self.nom == "":
            raise ValidationError("El nom no pot ser nul.")

    def __unicode__(self):
        return self.nom #+ u':' + unicode(self.dinici) + u',' + unicode(self.dfi)
            
class UFAvisos(models.Model):
  assignatura = models.ForeignKey(Assignatura, null=False, blank=False)
  alumne = models.ForeignKey(Alumne, null=False, blank=False)
  nAvis = models.PositiveSmallIntegerField(blank=False)