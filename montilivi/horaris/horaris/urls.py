from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from extHoraris import views 

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^extHoraris/', include('extHoraris.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', LoginView.as_view(template_name='login.html'), name='login'), #login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$',logout, {'next_page': '/'}, name='logout'),
    #Static files

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
