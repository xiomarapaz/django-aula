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
