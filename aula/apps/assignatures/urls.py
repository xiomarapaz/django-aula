from django.conf.urls import url
from aula.apps.assignatures import views

urlpatterns = [
    url(r'^$', views.seleccionarAssignatura, name="aula__materies__seleccionar_assignatura_uf"),
    url(r'^configurarNotificacions/(?P<idAssignatura>\d+)/$', views.configurarNotificacions, name="aula__materies__seleccionar_assignatura_uf"),
    url(r'^veureUnitatsFormatives/(?P<idAssignatura>\d+)/$', views.veureUnitatsFormatives, 
        name="aula__materies__seleccionar_assignatura_uf_veure" ),
    url(r'^crearUnitatFormativa/(?P<idAssignatura>\d+)/$', views.crearUnitatFormativa, 
        name="aula__materies__seleccionar_assignatura_uf_crear" ),
    url(r'^modificarUnitatFormativa/(?P<idAssignatura>\d+)/(?P<id>\d+)/$', views.modificarUnitatFormativa, 
        name="aula__materies__seleccionar_assignatura_uf_modificar" ),
    url(r'^eliminarUnitatFormativa/(?P<idAssignatura>\d+)/(?P<id>\d+)/$', views.eliminarUnitatFormativa, 
        name="aula__materies__seleccionar_assignatura_uf_eliminar" ),    
    url(r'^llistatAssistenciaEntreDates/$', views.llistatAssistenciaUFs, 
        name="aula__materies__llistat_assistencia_ufs" ),    
    
    #url(r'^testLlistatAssistenciaUFsDiscontinuades/$', 'llistatAssistenciaUFsDiscontinuades', 
    #    name="aula__materies__llistat_assistencia_ufs_discontinuades" ),    
]

