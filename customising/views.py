# This Python file uses the following encoding: utf-8

# templates
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# ---------------------  --------------------------------------------#

@login_required
def ajuda(request):
    return render(request,
        'ajuda.html',
        {})