from django.conf.urls import url
from aula.mblapp import views as mblapp_views

urlpatterns = [
    url(r'^hello_api/$', mblapp_views.hello_api,
        name='mblapp__hello__api'),
    url(r'^hello_api_login/$', mblapp_views.hello_api_login,
        name='mblapp__hello__apilogin'),
        
]