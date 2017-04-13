import pandas as pd
import requests
from bs4 import BeautifulSoup

#Leemos CSV que nos interesa para ir haciendo Crawl linea a linea
consorcio_lineasDF = pd.read_csv ('Consorcio_Lineas_Granada.csv',index_col = 'Unnamed: 0')
lineas = consorcio_lineasDF.NumLineaWeb.values

for linea in lineas:
    #print(linea)
    url = 'http://siu.ctagr.com/es/horarios_lineas_tabla.php?from=1&linea={}'.format(linea)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    #print(soup)

    horarios = soup.find(id = 'recorrido_din').find_all('table')
    ##print(horarios)

    if (len(horarios)>=2): #Hubo al menos una linea que solo tenia los datos de ida ,
                            #por lo tanto si no se mete este if
                            #daria error
        ida_horariosDF = pd.DataFrame()
        lista_nucleos = []
        lista_horarios = []
        control_segunda_cabecera = False
        

        ida_table = horarios[0].find_all('tr')
        for i,x in enumerate(ida_table):
            if i == 0: # Nombres de los pueblos de IDA
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                if (bool(x) == False): #Nos aseguramos de que ha cogido los valores que debia
                                       #Es porque en algunas tablas hay dos niveles para las cabeceras
                    control_segunda_cabecera = True
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (control_segunda_cabecera and (i==1)):#Nombre de los pueblos de ida si habia cabecera
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (not control_segunda_cabecera and (i >= 1)):#Horario pueblos ida
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []
            elif(control_segunda_cabecera and (i>=2)):#Horario de los pueblos de ida si habia cabecera
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []

        #print(ida_horariosDF)
        ida_horariosDF.to_csv('/{}_ida_horario_CTMGR.csv'.format(linea))

        vuelta_horariosDF = pd.DataFrame()
        lista_nucleos = []
        lista_horarios = []
        control_segunda_cabecera = False

        vuelta_table = horarios[1].find_all('tr')
        for i,x in enumerate(vuelta_table):
            if i == 0: # Nombres de los pueblos de IDA
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                if (bool(x) == False): #Nos aseguramos de que ha cogido los valores que debia
                                       #Es porque en algunas tablas hay dos niveles para las cabeceras
                    control_segunda_cabecera = True
                vuelta_horariosDF = vuelta_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (control_segunda_cabecera and (i==1)):#Nombre de los pueblos de ida si habia cabecera
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                vuelta_horariosDF = vuelta_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (not control_segunda_cabecera and (i >= 1)):#Horario pueblos ida
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                vuelta_horariosDF = vuelta_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []
            elif(control_segunda_cabecera and (i>=2)):#Horario de los pueblos de ida si habia cabecera
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                vuelta_horariosDF = vuelta_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []

        #print(vuelta_horariosDF)
        vuelta_horariosDF.to_csv('{}_vuelta_horario_CTMGR.csv'.format(linea))
    else:
        #print('La linea(numlineaweb ',linea,' solo tiene una tabla')
        ida_horariosDF = pd.DataFrame()
        lista_nucleos = []
        lista_horarios = []
        control_segunda_cabecera = False
        

        ida_table = horarios[0].find_all('tr')
        for i,x in enumerate(ida_table):
            if i == 0: # Nombres de los pueblos de IDA
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                if (bool(x) == False): #Nos aseguramos de que ha cogido los valores que debia
                                       #Es porque en algunas tablas hay dos niveles para las cabeceras
                    control_segunda_cabecera = True
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (control_segunda_cabecera and (i==1)):#Nombre de los pueblos de ida si habia cabecera
                x = x.find_all('div')
                num_nucleos = len(x)
                for nucleo in x:
                    lista_nucleos.append(nucleo.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_nucleos).T)
                lista_nucleos = []
            if (not control_segunda_cabecera and (i >= 1)):#Horario pueblos ida
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []
            elif(control_segunda_cabecera and (i>=2)):#Horario de los pueblos de ida si habia cabecera
                for d in x.find_all('td')[0:num_nucleos]:
                    lista_horarios.append(d.text)
                ida_horariosDF = ida_horariosDF.append(pd.DataFrame(lista_horarios).T)
                lista_horarios = []

        #print(ida_horariosDF)
        ida_horariosDF.to_csv('{}_ida_horario_CTMGR.csv'.format(linea))        
        
