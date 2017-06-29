import re
import requests

import sqlite3
import pandas as pd

from utilities.getting_soup_from_web import BSoup

def fill_db(bus_line, one_way_or_return, bus_line_stopsDF):
    '''FILL CONSORCIOGR.DB WITH ITINERARY FOR EACH BUS LINE'''
    db_name = '..\datos\ConsorcioGR.db'
    table_name = 'itinerary_{0}_{1}_CTMGR'.format(bus_line, one_way_or_return)
    conn_CTMGR = sqlite3.connect(db_name)
    bus_line_stopsDF.to_sql(table_name, conn_CTMGR, index= False)
    conn_CTMGR.commit()
    conn_CTMGR.close()

def obtain_itinerary(bus_line,itinerary_soup,id_way_or_return):
    '''CRAWL WEBPAGES AND FILLS DF WITH ITINERARIES'''
    bus_line_stopsDF = pd.DataFrame(columns=['bus_stop','lat','lon'])
    try:
        itinerary = itinerary_soup.find(id = id_way_or_return).find_all('a')
    except AttributeError:
        print('{0} LINEA RAISED SOME ERROR'.format(bus_line))
    else:
        for link in itinerary:
            coord_begin = int(re.search('\(',link['href']).start())
            coord_end = int(re.search('\)',link['href']).end())
            lat , lon = link['href'][coord_begin+1:coord_end-1].split(',')
            bus_stop_name = link.text

            bus_line_stopsDF = bus_line_stopsDF.append(pd.DataFrame(
                data=[[bus_stop_name,lat,lon]],columns=['bus_stop','lat','lon']))
##        bus_line_stopsDF.to_csv(
##            '{0}_{1}_itinerary_CTMGR.csv'.format(bus_line,id_way_or_return))
        fill_db(bus_line,  id_way_or_return,  bus_line_stopsDF)
        
def read_csv():
    '''READS CSV WITH GENERAL DATA NEEDED FOR CRAWLING AND RETURNS
       WEB_CODES FOR EACH LINE'''
    encoding_library = ['iso-8859-1',  'latin1',  'cp1252',  'utf-8']
    for encoding in encoding_library:
        try:
            consorcio_lineasDF = pd.read_csv (
                '..\datos\Consorcio_bus_lines_Granada.csv',
                index_col = 'Unnamed: 0',   encoding=encoding)
        except UnicodeDecodeError:
            print('Encoding with {0} didn\'t work'.format(encoding))
        else:
            print('Encoding with {0} succesful'.format(encoding))
            break
    return consorcio_lineasDF.bus_line_web_code.values

def main():
    '''GETS LIST OF WEB_CODES NEEDED TO CRAWL. FOR EACH LINE GETS ITS
    SOUP AND CALLS FUNCTION TO OBTAIN TIMETABLES'''
    lineas = read_csv()
    for linea in lineas:
        url = 'http://siu.ctagr.com/es/horarios_lineas_tabla.php?from=1&linea={0}'
        url = url.format(linea)
        itinerary_soup = BSoup(url)
        for id_way_or_return in ['paradas_ida',  'paradas_vuelta']:
            obtain_itinerary(linea,itinerary_soup, id_way_or_return)
main()
