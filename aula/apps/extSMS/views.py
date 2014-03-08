# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from aula.apps.extSMS.forms import smsForm
from models import extSMS

@login_required
def llistaSMS(request):
    #TODO:
    #Fer que no surti el numero
    #Treballar amb multiples formularis

    if request.method == 'POST':

        form = smsForm(request.POST)
        print form
        if form.is_valid():
            if form.cleaned_data['envia']:
                try:
                    extSMS.objects.get(incidencia=form.cleaned_data['incidencia']).delete()
                except extSMS.DoesNotExist:
                    pass

    totsSMS = extSMS.objects.all()
    formularis = []
    #Crear el formulari per cada sms i fotre'l al array
    for sms in totsSMS:
        formularis.append(smsForm(instance=sms))


    return render(request, 'mostraSMS.html', {'formularis': formularis})


