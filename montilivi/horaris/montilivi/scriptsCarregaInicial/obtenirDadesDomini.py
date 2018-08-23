# - encoding: utf-8 #
# Script per obtenir els usuaris del domini de Montilivi.

import requests
import codecs
import cStringIO
import lxml.html
import csv

def imprimirCSV(usuaris, pathFitxer):
  """
    Rep una llista d'usuaris on cada entrada té una subllista amb el nom i el cognom.
    imprimeix en un CSV.
  """
  with open(pathFitxer, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for usuari in usuaris:
      fila = []
      for dada in usuari:
        fila.append(dada.encode('utf-8'))
      spamwriter.writerow(fila)

def obtenirLlistaUsuaris(html):
  #Passo les dades a text utf, ignorant alguns errors de la weppe.
  #dades=html.decode('utf-8', 'ignore')
  fitxerAParsejar = cStringIO.StringIO(html.encode('utf-8'))
  html = lxml.html.parse(fitxerAParsejar)
  #Només hi hauria d'haver una sola taula.
  
  usuarisCorrectes =[]
  tbl=html.xpath('//table/tbody')[0]
  trs=tbl.getchildren()
  for tr in trs:
    tds=tr.getchildren()
    tdCounter=0
    usuariActual=[]
    for td in tds:
      #Només llegiré les dues primeres columnes.
      if tdCounter < 2:
        usuariActual.append(td.text_content().strip())
      tdCounter+=1
    if len(usuariActual) == 2:
      if usuariActual[0] != '' and usuariActual[1] != '':
        usuariActual.reverse()
        usuarisCorrectes.append(usuariActual)
  return usuarisCorrectes

usuari = raw_input("Entra el nom de l\'usuari per accedir al domini de montilivi:")
password = raw_input("Entra el password de l\'usuari:")

formdata = { "_username" : usuari, "_password": password, "login": "" }
with requests.Session() as s:
  r = s.get('https://www.institutmontilivi.cat/intranet/', verify=False)
  r = s.post('https://www.institutmontilivi.cat/intranet/login_check',  
    data=formdata, verify=False)
  print r.status_code
  print r.url
  f = codecs.open('output.html','w', 'utf-8')
  f.write(r.text)
  f.close()
  
  llistaProfes=[]
  
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/Administratiu@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/automocio@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/electronica@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/FOL@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/informatica@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/quimica@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/seguretatimediambient@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  r = s.get('https://www.institutmontilivi.cat/intranet/aplicacions-administratives/llistes-distribucio/membres-del-grup/serveisalacomunitat@institutmontilivi.cat/', verify=False)
  llistaProfes = llistaProfes + obtenirLlistaUsuaris(r.text)
  imprimirCSV(llistaProfes, '/var/dadesProtegides/horaris/profes/profes.csv')


