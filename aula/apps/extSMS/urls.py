from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('aula.apps.extSMS.views',
                       
   url(r'^$', 'llistaSMS' ,
       name="llista-sms"),
)

