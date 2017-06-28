import pandas as pd
import sqlite3

from utilities.getting_soup_from_web import BSoup

def fill_db(bus_line, one_way_or_return, timetableDF):
    '''FILL CONSORCIOGR.DB WITH TIMETABLE FOR EACH BUS LINE'''
    db_name = 'ConsorcioGR.db'
    table_name = 'timetable_{0}_{1}_CTMGR'.format(bus_line, one_way_or_return)
    conn_CTMGR = sqlite3.connect(db_name)
    timetableDF.to_sql(table_name, conn_CTMGR, index= False)
    conn_CTMGR.commit()
    conn_CTMGR.close()
    
def crawl_timetables(bus_line, timetable, one_way_or_return):
    '''CRAWL WEBPAGES AND FILLS DF WITH TIMETABLES'''
    timetableDF = pd.DataFrame()
    bus_line_stops = []
    timetable_list = []
    second_header_control = False
    for i,x in enumerate(timetable):
        if i == 0:
            # Town names
            x = x.find_all('div')
            bus_line_stops_len = len(x)
            for bus_line_stop in x:
                bus_line_stops.append(bus_line_stop.text)
            if (bool(x) == False):
                #Some tables have two header levels
                second_header_control = True
            timetableDF = timetableDF.append(
                pd.DataFrame(bus_line_stops).T)
            bus_line_stops = []
        if (second_header_control and (i == 1)):
            #Town name in case there was header
            x = x.find_all('div')
            bus_line_stops_len = len(x)
            for bus_line_stop in x:
                bus_line_stops.append(bus_line_stop.text)
            timetableDF = timetableDF.append(
                pd.DataFrame(bus_line_stops).T)
            bus_line_stops = []
        if (not second_header_control and (i >= 1)):
            #Timetable 
            for d in x.find_all('td')[0:bus_line_stops_len]:
                timetable_list.append(d.text)
            timetableDF = timetableDF.append(
                pd.DataFrame(timetable_list).T)
            timetable_list = []
        elif(second_header_control and (i>=2)):
            #Timetable in case there was header
            for d in x.find_all('td')[0:bus_line_stops_len]:
                timetable_list.append(d.text)
            timetableDF = timetableDF.append(
                pd.DataFrame(timetable_list).T)
            timetable_list = []
##    timetableDF.to_csv(csv_name)
    fill_db(bus_line, one_way_or_return, timetableDF)

def obtain_timetables (timetable_soup, bus_line, one_way_or_return):
    '''CHECK THAT IT IS POSSIBLE TO CRAWL AND CALLS CRAWLING FUNCTION
       PASSING IT THE RIGHT SOUP(ONE_WAY OR RETURN)'''
    try:
        if one_way_or_return == 'oneway':
            timetable = timetable_soup[0].find_all('tr')
        elif one_way_or_return == 'return':
            timetable = timetable_soup[1].find_all('tr')
    except IndexError:
        file_name = 'filling_consorcio_db_log.txt'
        with open(file_name, 'r+') as f_obj:
            f_obj.write('\nLine {0} NOT FOUND FOR RETURN WAY')
    else:
        crawl_timetables(bus_line, timetable, one_way_or_return)
        
def read_csv():
    '''READS CSV WITH GENERAL DATA NEEDED FOR CRAWLING AND RETURNS
       WEB_CODES FOR EACH LINE'''
    encoding_library = ['iso-8859-1',  'latin1',  'cp1252',  'utf-8']
    for encoding in encoding_library:
        try:
            consorcio_bus_linesDF = pd.read_csv (
                '..\datos\Consorcio_bus_lines_Granada.csv',
                index_col = 'Unnamed: 0',  encoding='iso-8859-1')
        except UnicodeDecodeError:
            print('Encoding with {0} didn\'t work'.format(encoding))
        else:
            print('Encoding with {0} succesful'.format(encoding))
            break
    return consorcio_bus_linesDF.bus_line_web_code.values
    
def main():
    '''GETS LIST OF WEB_CODES NEEDED TO CRAWL. FOR EACH LINE GETS ITS
       SOUP AND CALLS FUNCTION TO OBTAIN TIMETABLES ONE OR TWO TIMES
       (DEPENDING ON IF THERE IS RETURN OR NOT'''
    bus_lines = read_csv()
    for bus_line in bus_lines:
        print(bus_line)
        url = 'http://siu.ctagr.com/es/horarios_lineas_tabla.php?from=1&linea={0}'
        url = url.format(bus_line)
        soup = BSoup(url)
        timetable_soup = soup.find(id = 'recorrido_din').find_all('table')
        
        if (len(timetable_soup)>=2):
            #Some lines only have one_way data
            obtain_timetables(timetable_soup, bus_line, 'oneway')
            obtain_timetables(timetable_soup, bus_line, 'return')

        else:       
            obtain_timetables(timetable_soup, bus_line, 'oneway')
    
main()
