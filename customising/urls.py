from django.conf.urls import url
from customising import views

urlpatterns = [
    url(r'ajuda/$', views.ajuda, name="varis__ajuda__ajuda") #el nom fa que sigui custom.
]