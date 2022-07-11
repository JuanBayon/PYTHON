from selenium import webdriver
import time
import re
import os, sys
import pandas as pd


ruta = os.path.abspath(__file__)
for i in range(3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

class Web_scraper():


    def __init__(self):
        self.restaurantes = {'nombre': [], 'ciudad': [], 'direccion': [], 'latitud': [], 'longitud': []}
        chrome_driver_path = ruta + os.sep + 'resources' + os.sep + 'chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        self.driver = driver
        self.dataframe = None


    def scraping(self, lista_url):
        """
        lista_url = {ciudad: [], url: []}
        
        """

        for i, (url, ciudad) in enumerate(zip(lista_url['url'], lista_url['ciudad'])):
            if i == 0:
                self.driver.get(url)
            else:
                self.driver.execute_script('window.open("'+url+'");') 
                self.driver.switch_to_window(self.driver.window_handles[-1]) 
            numero_paginas = []
            span = self.driver.find_elements_by_tag_name('li')
            for texto in span:
                if bool(re.search('Página', str(texto.text))):
                    numero_paginas.append(texto.text)
            num_pag = int(numero_paginas[0].split()[-1])

            for i in range(1, num_pag + 1):
                if i == 1:
                    ruta = url
                else:
                    ruta = url + os.sep + str(i)
                self.driver.execute_script('window.open("'+ruta+'");') 
                self.driver.switch_to_window(self.driver.window_handles[-1]) 
                restaurantes_pagina = self.driver.find_elements_by_class_name('listing-item-title')
                lista = [rest.text for rest in restaurantes_pagina]
                links_rest = []
                for l in lista:
                    http = self.driver.find_elements_by_link_text(l)[0].get_attribute('href')
                    links_rest.append(http)
                for link, name in zip(links_rest, lista):
                    self.driver.execute_script('window.open("'+link+'");') 
                    self.driver.switch_to_window(self.driver.window_handles[-1]) 
                    time.sleep(5)
                    links = self.driver.find_elements_by_tag_name('a')
                    lista_links = [lnk.get_attribute('href') for lnk in links]
                    mapa = []
                    for link in lista_links:
                        if bool(re.search('maps.google', str(link))):
                            mapa.append(link)
                    a = mapa[0].split('=')
                    b = a[-1].split(',')
                    latitud = float(b[0])
                    c = b[-1].split('%20')
                    longitud = float(c[-1])
                    direccion = self.driver.find_elements_by_css_selector('p')
                    lista_direcciones = [dire.text for dire in direccion]
                    adress = []
                    for dire in lista_direcciones:
                        if bool(re.search('España', str(dire))) and bool(re.search(f'{ciudad}', str(dire))):
                            adress.append(dire)
                    self.restaurantes['latitud'].append(latitud)
                    self.restaurantes['longitud'].append(longitud)
                    self.restaurantes['direccion'].append(adress[0])
                    self.restaurantes['nombre'].append(name)
                    self.restaurantes['ciudad'].append(ciudad)
                    self.driver.close()
                    self.driver.switch_to_window(self.driver.window_handles[0])

                    self.dataframe = pd.DataFrame(self.restaurantes)

                print (f'La página {i} de {ciudad} se ha registrado correctamente.')
                self.driver.close()
                self.driver.switch_to_window(self.driver.window_handles[0])

        print('Proceso finalizado con éxito')