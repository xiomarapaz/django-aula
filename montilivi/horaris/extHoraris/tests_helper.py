#encoding: utf-8

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from extHoraris.models import Grup
import sys
from typing import List

class Pagina(object):
    def __init__(self, driver, live_server_url):
        #type: (Firefox, str)->None
        self.driver = driver #type: Firefox
        self.live_server_url = live_server_url
        
        
class PaginaLogin(Pagina):
    
    def dologin(self):
         #Test que comprova el funcionament de la vista índex.
        
        html = self.driver.get(self.live_server_url)
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        username.clear()
        username.send_keys("horaris")
        password.clear()
        password.send_keys("horaris")
        boto = self.driver.find_element_by_xpath('//input[@type="submit"]')
        boto.click()

class SeleccioGrup(Pagina):

    def __init__(self, driver, live_server_url):
        #type: (Firefox, str)->None
        super(SeleccioGrup, self).__init__(driver, live_server_url)
        self.html = self.driver.get(self.live_server_url + "/extHoraris")

    def getGroups(self):
        elem = self.driver.find_element_by_name("idGrup")
        self.conjuntOpcions = elem.find_elements_by_tag_name("option")
        return self.conjuntOpcions

    def clickOpcio(self, opcio):
        #type:(FirefoxWebElement)->None
        opcio.click()

    def submit(self):
        #type:(FirefoxWebElement)->None
        boto = self.driver.find_element_by_xpath("//button[@type='submit']")
        boto.click()

class AfegirHorari(Pagina):

    def __init__(self, driver, live_server_url, idGrup):
        #type: (Firefox, str)->None
        super(AfegirHorari, self).__init__(driver, live_server_url)
        #Obtenir l'ID del grup.
        self.html = self.driver.get(self.live_server_url + "/extHoraris/calendari/" + idGrup)

    def obtenirElementsSelect(self, nomSelect):
        #type: (str)->List[FirefoxWebElement]
        #retornar llistat opcions d'un select.
        elem = self.driver.find_element_by_name(nomSelect)
        self.conjuntOpcions = elem.find_elements_by_tag_name("option")
        return self.conjuntOpcions

    def seleccionarElement(self, opcio):
        #type: (FirefoxWebElement)->None
        opcio.click()

    def inserirText(self, nomTxtBox, text):
        elem = self.driver.find_element_by_name(nomTxtBox) #type: FirefoxWebElement
        elem.clear()
        elem.send_keys(text)

    def enviar(self):
        boto = self.driver.find_element_by_xpath("//button[@type='submit']")
        boto.click()

    def obtenirIdNomSelect(self, opcio):
        #type: (FirefoxWebElement)->(str, str)
        nom = opcio.text
        id = opcio.get_attribute("value")
        return id, nom

