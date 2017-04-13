# consorcioTransportesGranada
Repositorio con distintos módulos que permite scrapear la web del [Consorcio de Transportes de Granada](http://www.ctagr.com/index.php?id=155) para obtener información sobre horarios e itinerarios.

Este modulo contiene una serie de scripts que permiten obtener la información publicada en la página web del [Consorcio de Transporte Metropolitano del área de Granada](http://www.ctagr.com/index.php?id=155) relativa a horarios e itinerarios de las distintas líneas que operan el servicio de transporte interurbano entre Granada y su área Metropolitana. Así mismo contiene archivos en formato .csv con información 

### Modulos de scraping
Este repositorio consiste de 3 módulos: 
  Primer modulo: permite obtener información sobre cada una de las líneas que son operadas por el Consorcio de Transportes, con el que sacamos información sobre Nombre de Linea y empresa concesionaria, así como la información necesaria para realizar el posterior scrapeo línea a línea.
  Segundo modulo: hacemos "scrapping" a los horarios de cada línea utilizando links obtenidos con el primer módulo.
  Tercer modulo:  hacemos "scrapping" a los itinerarios de cada línea utilizando links obtenidos con el primer módulo.

Al correr el segundo y tercer módulo se obtiene un archivo .csv para cada trayecto y línea  (dos archivos de horarios por linea y otros dos de itinerario por linea). El nombre del archivo en cada caso empieza con el "número utilizado para identificar la web que hay scrapear en cada caso. Se puede ver la correspondencia de este numero con el número oficial de la línea en el archivo Consorcio_Lineas_Granada.csv.

### Datos
Los datos publicados utilizando los modulos de scrapeo anteriormente mencionados son de 03/2017, por lo que no contemplan variaciones posteriores que el consorcio haya realizado sobre los mismos
