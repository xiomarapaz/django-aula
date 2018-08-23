from django.conf.urls import url
from extHoraris import views, profes, aules
from django.contrib.auth.views import logout
from extHoraris import views

urlpatterns = (
    url(r'^$', views.index, name='extHoraris__index'),
    url(r'^calendari/(?P<idGrup>[0-9]+)$', views.calendari, name='extHoraris__calendari'),
    url(r'^calendari/afegirEntradaHorari$', views.afegirEntradaHorari, name='extHoraris__afegirEntradaHorari'),
    url(r'^calendari/veureEntradaHorari/(?P<idEntrada>[0-9]+)$', views.veureEntradaHorari, name='extHoraris__veureEntradaHorari'),
    url(r'^calendari/eliminarEntradaHorari/(?P<idEntrada>[0-9]+)$', views.eliminarEntradaHorari, name='extHoraris__eliminarEntradaHorari'),
    url(r'^calendari/modificarEntradaHorari$', views.modificarEntradaHorari, name='extHoraris__modificarEntradaHorari'),
    url(r'^calendari/imprimirHorariGrup/(?P<idGrup>[0-9]+)$', views.imprimirHorariGrup, name='extHoraris__imprimirHorariGrup'),
    url(r'^calendari/imprimirHorariProfes$', views.imprimirHorariProfes, name='extHoraris__imprimirHorariProfes'),
    url(r'^calendari/imprimirHorariProfe/(?P<idProfe>[0-9]+)$', views.imprimirHorariProfe, name='extHoraris__imprimirHorariProfe'),
    url(r'^calendari/imprimirHorariAules$', views.imprimirHorariAules, name='extHoraris__imprimirHorariAules'),
    url(r'^calendari/imprimirHorariAula/(?P<idAula>.+)$', views.imprimirHorariAula, name='extHoraris__imprimirHorariAula'),
    url(r'^calendari/imprimirCsv/$', views.imprimirCsv, name='extHoraris__imprimirCsv'),
    url(r'^calendari/carregarCsvProfes/$', views.carregarCsvProfes, name='extHoraris__carregarCsvProfes'),
    #Manteniments profes.
    url(r'^profe$', profes.ProfeList.as_view(), name='profe_list'),
    url(r'^profe/new$', profes.ProfeCreate.as_view(), name='profe_new'),
    url(r'^profe/edit/(?P<pk>\d+)$', profes.ProfeUpdate.as_view(), name='profe_edit'),
    url(r'^profe/delete/(?P<pk>\d+)$', profes.ProfeDelete.as_view(), name='profe_delete'),
    #Manteniments aules.
    url(r'^aula$', aules.AulaList.as_view(), name='aula_list'),
    url(r'^aula/new$', aules.AulaCreate.as_view(), name='aula_new'),
    url(r'^aula/delete/(?P<pk>\d+)$', aules.AulaDelete.as_view(), name='aula_delete'),
)
