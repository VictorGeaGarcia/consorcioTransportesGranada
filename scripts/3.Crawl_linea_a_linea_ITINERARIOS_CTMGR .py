import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#Leemos CSV que nos interesa para ir haciendo Crawl linea a linea
consorcio_lineasDF = pd.read_csv ('Consorcio_Lineas_Granada.csv',index_col = 'Unnamed: 0')


#Hacemos un crawl primero a cualquiera de las lineas para ver exacatamente que hay que
#extraer en cada caso

lineas = consorcio_lineasDF.NumLineaWeb.values
##for linea in lineas:
##    print(linea)


###
###   TODO LO DE ABAJO HAY QUE METERLO EN EL FOR QUE HAY JUSTO ARRIBA (for linea in lineas)
###

   #########################################################################################

for linea in lineas:
##    print('Estamos en la linea: ',linea)
    url = 'http://siu.ctagr.com/es/horarios_lineas_tabla.php?from=1&linea={}'.format(linea)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
##    print(soup)


    ida_lineaDF = pd.DataFrame(columns=['Parada','Lat','Lon'])

    itinerario_ida = soup.find(id = 'paradas_ida').find_all('a')
    paradas_ida = []
    ind = 0
##    print('IDA')
    for link in itinerario_ida:

        inicio_coord = int(re.search('\(',link['href']).start())
        fin_coord = int(re.search('\)',link['href']).end())
        lat , lon = link['href'][inicio_coord+1:fin_coord-1].split(',')
        nom_parada = link.text
        paradas_ida.append(nom_parada)
        
        ida_lineaDF = ida_lineaDF.append(pd.DataFrame(data=[[nom_parada,lat,lon]],columns=['Parada','Lat','Lon']))
        ind =+ 1    
##        print(link['href'])
##        print('Lat: ',lat,' Lon: ',lon)
##        print('La parada es :',nom_parada)

    ida_lineaDF.to_csv('{}_ida_itinerario_CTMGR.csv'.format(linea))
        
    vuelta_lineaDF = pd.DataFrame(columns=['Parada','Lat','Lon'])

    itinerario_vuelta = soup.find(id = 'paradas_vuelta').find_all('a')
    paradas_vuelta = []
##    print('VUELTA')
    for link in itinerario_vuelta:

        inicio_coord = int(re.search('\(',link['href']).start())
        fin_coord = int(re.search('\)',link['href']).end())
        lat , lon = link['href'][inicio_coord+1:fin_coord-1].split(',')
        nom_parada = link.text
        paradas_vuelta.append(nom_parada)
        
        vuelta_lineaDF = ida_lineaDF.append(pd.DataFrame(data=[[nom_parada,lat,lon]],columns=['Parada','Lat','Lon']))
        ind =+ 1    
##        print(link['href'])
##        print('Lat: ',lat,' Lon: ',lon)
##        print('La parada es :',nom_parada)

##    print(vuelta_lineaDF)
    vuelta_lineaDF.to_csv('{}_vuelta_itinerario_CTMGR.csv'.format(linea))
