from django.conf.urls import url
from aula.mblapp import views as mblapp_views

urlpatterns = [
    url(r'^hello_api/$', mblapp_views.hello_api,
        name='mblapp__hello__api'),
    url(r'^hello_api_login/$', mblapp_views.hello_api_login,
        name='mblapp__hello__apilogin'),
    url(r'^hello_api_login_app/$', mblapp_views.hello_api_login_app,
        name='mblapp__hello__apiloginapp'),        
    url(r'^capture_token_api/$', mblapp_views.capture_token_api,
        name='mblapp__api__capture_token_api'),        
]