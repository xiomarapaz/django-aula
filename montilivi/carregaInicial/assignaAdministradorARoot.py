#encoding: utf-8

from django.contrib.auth.models import User, Group

g = Group.objects.get( name = 'direcció' )
a = User.objects.get( username = 'root' )
a.groups = [ g ]
a.save()
quit()