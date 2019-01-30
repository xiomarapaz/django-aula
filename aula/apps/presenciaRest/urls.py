from django.conf.urls import url
from aula.apps.presenciaRest import views

urlpatterns = [
    url(r'^ajuda/$', views.ajuda),
    url(r'^login/(?P<idUsuari>[A-Za-z0-9]+)/$', views.login),
    url(r'^getImpartirPerData/(?P<paramData>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<idUsuari>[A-Za-z0-9]+)/$',
        views.getImpartirPerData),
    url(r'^getControlAssistencia/(?P<idImpartir>[0-9]+)/(?P<idUsuari>[A-Za-z0-9]+)/$', views.getControlAssistencia),
    url(r'^putControlAssistencia/(?P<idImpartir>[0-9]+)/(?P<idUsuari>[A-Za-z0-9]+)/$', views.putControlAssistencia),
    url(r'^getFrangesHoraries/(?P<idUsuari>[A-Za-z0-9]+)/$', views.getFrangesHoraries),
    url(r'^test/', views.test),
    ]

'''
    url(r'^controlimpartirdetail/(?P<idImpartir>[0-9]+)/(?P<idUsuari>[0-9]+)/$', 'controlImpartirDetail',
        name="controlImpartirDetail"),
    url(r'^professorbylogin/(?P<loginUsuari>[a-z|A-Z|\.]+)/$', 'professorByLogin',
        name="professorByLogin"),
    url(r'^frangeshorarieslist/(?P<idUsuari>[0-9]+)/$', 'frangesHorariesList',
        name="frangesHorariesList"),
    url(r'^profeslist/(?P<idUsuari>[0-9]+)/$', 'profesList',
        name="profesList"),
    url(r'^creaguardia/(?P<idUsuariSubstitut>[0-9]+)/$', 'creaGuardia',
        name="creaGuardia")'''