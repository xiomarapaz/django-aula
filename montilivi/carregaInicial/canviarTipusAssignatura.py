from aula.apps.alumnes.models import Nivell
from aula.apps.assignatures.models import TipusDAssignatura
from aula.apps.assignatures.models import Assignatura
uf = TipusDAssignatura.objects.get( tipus_assignatura = 'Unitat Formativa' )
for n  in Nivell.objects.all():
   print 'Canviant nivell' + unicode(n)
   for a in Assignatura.objects.filter( curs__in = n.curs_set.all()):
      print 'canviant assignatura' + unicode(a)
      a.tipus_assignatura = uf
      a.save()