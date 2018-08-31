# This Python file uses the following encoding: utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http.response import *
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms import ValidationError

from extHoraris.models import *


class AulaForm(forms.ModelForm):
    """
    Classe encarregada de fer la validació d'una aula.
    """
    nom = forms.CharField(max_length=50, label='Nom Aula')

    def clean_nom(self):
        nom = self.cleaned_data['nom']

        if (len(nom) == 0):
            raise ValidationError("Cal introduir un valor.")

        return nom

    class Meta:
        model = Aula
        fields = ['nom']


class AulaList(ListView):
    #model = Profe
    queryset = Aula.objects.order_by('nom')

    def get_context_data(self, **kwargs):
        # Obtenir el context de la base per modificar-lo i afegir-hi dades.
        context = super(AulaList, self).get_context_data(**kwargs)
        # Obtenir a quin horari hem de tornar quan ens ho demanen.
        context = addVariablesToContext(context, self.request)
        return context

class AulaCreate(CreateView):
    model = Aula
    success_url = reverse_lazy('aula_list')
    form_class = AulaForm

    def get_context_data(self, **kwargs):
        context = super(AulaCreate, self).get_context_data(**kwargs)
        context = addVariablesToContext(context, self.request)
        return context

class AulaDelete(DeleteView):
    model = Aula
    success_url = reverse_lazy('aula_list')

    def get_context_data(self, **kwargs):
        context = super(AulaDelete, self).get_context_data(**kwargs)
        context = addVariablesToContext(context, self.request)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        except Exception:
            return render_to_response("extHoraris/aula_error.html", {
                'errormsg': 'Error al eliminar una aula que ja té hores assignades. ',
                'idRetornHoraris': request.session.get('HorarisRetorn'),
            },
            context_instance=RequestContext(request))

def addVariablesToContext(context, request):
    context['idRetornHoraris'] = request.session.get('HorarisRetorn')
    return context