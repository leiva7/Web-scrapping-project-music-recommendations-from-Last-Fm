# Web sctraping proyect: getting some music recomendations from Last.Fm :headphones: :musical_note:
# Proyecto web scraping: obteniendo recomendaciones musicales de Last.Fm :headphones: :musical_note:


## En qué consiste el proyecto
En este proyecto se utiliza la librería BeautifulSoup de python para scrapear el sitio Last.fm. 
La persona que ejecute el archivo [extraerLastFM - funciones.py](extraerLastFM - funciones.py) pordrá ver un menú para seleccionar un estilo musical. A partir de dicha selección, el programa recorrerá las canciones que Last.Fm tiene publicadas bajo esa etiqueta, y a con base en la información recogida construirá, sobre una plantilla que es parte del proyecto, una página por canción con: el nombre del autor y la canción, el link al video de youtube de la canción, los tres autores similares que recomienda Last.Fm, la búsqueda de información sobre la banda en un iframe de wikipedia, y un widget integrado de https://www.listube.com/ para escuchar música en la misma página. 
Cada una de las páginas tendrá un menú de navegación que lleva a todas las demás. 
Además salva la información scrapeada en un archivo .csv

## What is the project about
This project uses the BeautifulSoup python library to scrape the Last.fm site.
The person running the file [extractLastFM - functions.py] (extractLastFM - functions.py) will see a menu to select a music style. From this selection, the program will go through the songs that Last.Fm has published under that label, and based on the information collected it will build, on a template that is part of the project, a page per song with: the name of the author and the song, the link to the song's youtube video, the three similar authors recommended by Last.Fm, the search for information about the band in a wikipedia iframe, and a built-in widget from https://www.listube.com / to listen to music on the same page.
Each of the pages will have a navigation menu that leads to all the others.
It also saves the scraped information in a .csv file.



## Motivos 
El proyecto lo realicé para resolver una consigna sobre scrapeo de 3er año de la tecnicatura en programación del ITS Córdoba; la temática musical fue elegida por mero placer, y la propuesta concreta toma forma ya que consideraba una linda manera de relajarse el poder explorar nuevas canciones y/o bandas de una manera sencilla y basada en el acceso a las 3 recomendaciones "si te gustó esto" y a contar con un reproductor e información sobre la banda en el mismo espacio. 

## Reasons
I carried out the project to solve an assignment on scraping for the 3rd year of the programming technician at ITS Córdoba; the musical theme was chosen for mere pleasure, and the  proposal is made because I considered a nice way to relax to be able to explore new songs and / or bands in a simple way and based on access to the 3 recommendations "if you liked this "and to have a player and information about the band in the same space.



## Aprendizajes
En el proceso afiancé conocimientos sobre Python, aprendí sobre las librerías urllib.request, csv, BeautifulSoup y webbrowser

## Learnings
In the process I strengthened my knowledge of Python, I learned about the urllib.request, csv, BeautifulSoup and webbrowser libraries


