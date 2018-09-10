# This Python file uses the following encoding: utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http.response import *
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms import ValidationError

from extHoraris.models import *


class ProfeForm(forms.ModelForm):
    """
    Classe encarregada de fer la validació d'un profe.
    """
    nomUsuari = forms.CharField(max_length=50, label='Identificador usuari')

    def clean_nomUsuari(self):
        nomUsuari = self.cleaned_data['nomUsuari']

        if (len(nomUsuari) == 0):
            raise ValidationError("Cal introduir un valor.")

        if ' ' in nomUsuari:
            raise ValidationError("El nom d'usuari no pot contenir espais.")

        if nomUsuari.lower() != nomUsuari:
            raise ValidationError("El nom d'usuari cal que estigui en minúscules")

        return nomUsuari

    class Meta:
        model = Profe
        fields = ['nomUsuari', 'nomComplert']


class ProfeList(ListView):
    #model = Profe
    queryset = Profe.objects.order_by('nomUsuari')

    def get_context_data(self, **kwargs):
        # Obtenir el context de la base per modificar-lo i afegir-hi dades.
        context = super(ProfeList, self).get_context_data(**kwargs)
        # Obtenir a quin horari hem de tornar quan ens ho demanen.
        context = addVariablesToContext(context, self.request)
        return context

class ProfeCreate(CreateView):
    model = Profe
    success_url = reverse_lazy('profe_list')
    form_class = ProfeForm
    
    def get_context_data(self, **kwargs):
        context = super(ProfeCreate, self).get_context_data(**kwargs)
        context = addVariablesToContext(context, self.request)
        return context

class ProfeUpdate(UpdateView):
    model = Profe
    success_url = reverse_lazy('profe_list')

    def get_context_data(self, **kwargs):
        context = super(ProfeUpdate, self).get_context_data(**kwargs)
        context = addVariablesToContext(context, self.request)
        return context

class ProfeDelete(DeleteView):
    model = Profe
    success_url = reverse_lazy('profe_list')

    def get_context_data(self, **kwargs):
        context = super(ProfeDelete, self).get_context_data(**kwargs)
        context = addVariablesToContext(context, self.request)
        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        except Exception:
            return render(request, "extHoraris/profe_error.html", {
                'errormsg': 'Error al eliminar un professor que ja té hores assignades. ',
                'idRetornHoraris': request.session.get('HorarisRetorn'),
            })
def addVariablesToContext(context, request):
    context['idRetornHoraris'] = request.session.get('HorarisRetorn')
    return context
