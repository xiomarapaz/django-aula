from aula.apps.usuaris.models import Professor
usuarisNoActius=Professor.objects.filter(is_active=False)
for usuari in usuarisNoActius:
    usuari.is_active = True
    print ("Activo", usuari)
    usuari.save()

