import pandas as pd
import requests
from bs4 import BeautifulSoup


#WEB CRAWLING A LA PAGINA GENERAL DE CTMGRANADA PARA SACAR INFO DE
#LAS LINEAS PARA DESPUES PODER HACERLE UN CRAWLING A CADA UNA DE ELLAS

#Preparamos el DF
consorcio_lineasDF = pd.DataFrame(columns=['Web','NumLineaWeb','Numero Linea','Nombre Linea','Empresa'])

#Crawl a URL, limpieza y pase a BeautifulSoup
url_todas_lineas = 'http://siu.ctagr.com/es/lineas.php'
source_code_todas_lineas = requests.get(url_todas_lineas)
plain_text_todas_lineas = source_code_todas_lineas.text
soup_todas_lineas = BeautifulSoup(plain_text_todas_lineas)
soup_todas_lineas = soup_todas_lineas.find_all('li','cercanias')

#Recorremos una a una las lineas y las metemos en el DF
index = 0
for linea in soup_todas_lineas:
    web = linea.find('a').get('href').strip()
    numlineaweb = (linea.find('a').get('href').strip().split('linea='))[1]
    numero_linea = (linea.find_all('span','grid_2'))[1].text.strip()
    nombre_linea = linea.find('span','grid_5 destacado').text.strip()
    empresa = linea.find('span','grid_4').text.strip()
    consorcio_lineasDF.loc[index] = [web,numlineaweb,numero_linea,nombre_linea,empresa]
    index +=1

#Imprimimos y sacamos CSV
print(consorcio_lineasDF)
consorcio_lineasDF.to_csv('Consorcio_Lineas_Granada.csv')




