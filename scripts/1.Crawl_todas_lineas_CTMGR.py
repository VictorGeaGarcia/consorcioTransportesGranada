import sqlite3
import pandas as pd

from utilities.getting_soup_from_web import BSoup

def consorcio_db(consorcio_bus_linesDF):
    '''DB CREATION WHERE GENERAL DATA ABOUT LINES IS INSERTED'''
    conn_CTMGR = sqlite3.connect('..\datos\ConsorcioGR.db')
    table_name = 'crawling_info_CTMGR'
    
    consorcio_bus_linesDF.to_sql(table_name,  conn_CTMGR, index = False)
    conn_CTMGR.commit()
    conn_CTMGR.close()
    
def crawl_general_CTMGR():
    '''WEB CRAWLING A LA PAGINA GENERAL DE CTMGRANADA PARA SACAR INFO DE
       LAS bus_lineS PARA DESPUES PODER HACERLE UN CRAWLING A CADA UNA
       DE ELLAS'''
    #Get DF ready
    consorcio_bus_linesDF = pd.DataFrame(
        columns=['url','bus_line_web_code',  'bus_line_number',  'bus_line_name',
                 'bus_line_enterprise'])

    url = 'http://siu.ctagr.com/es/lineas.php'
    soup = BSoup(url)
    soup = soup.find_all('li', 'cercanias')

    #Iterate over bus_lines and insert them into the DF
    index = 0
    for bus_line in soup:
        url = bus_line.find('a').get('href').strip()
        bus_line_web_code = bus_line.find('a').get('href').strip()
        bus_line_web_code = (bus_line_web_code.split('linea='))[1]
        bus_line_number = (bus_line.find_all('span',  'grid_2'))[1].text.strip()
        bus_line_name = bus_line.find('span',  'grid_5 destacado').text.strip()
        bus_line_enterprise = bus_line.find('span',  'grid_4').text.strip()
        consorcio_bus_linesDF.loc[index] = [url,  bus_line_web_code,
                                            bus_line_number,  bus_line_name,
                                            bus_line_enterprise]
        index +=1

    #Insert values to db
    #print(consorcio_bus_linesDF)
    consorcio_db(consorcio_bus_linesDF)


crawl_general_CTMGR()

