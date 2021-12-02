import urllib
import urllib.request
import csv
from bs4 import BeautifulSoup
import webbrowser

def bajar(url):
    """
Esta función toma una dirección de Internet y devuelve la página como un objeto BeautifulSoup, es decir el código fuente de la página en un formato que facilita
la extracción de información.
    """
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req)
    return BeautifulSoup(r.read())

def cancionesTablaPagTag(sopa):
    """
Extrae los nombres de las canciones en la tabla de alguno de los sitios de last.fm con formato /tag/... y devolverlos en lista. Para eso toma la sopa del sitio con el formato indicado (ej de sitio: "https://www.last.fm/es/tag/acoustic/tracks")
    """
    titulosFilas = sopa.findAll("td", {"class": "chartlist-name"})
    titulos = []
    for f in titulosFilas:
        a = f.find("a")
        titulos.append(a.text)
    #titlesText = sopa.find_all("a")
    return(titulos)

def artistasTablaPagTag(sopa):
    """
Extrae los nombres de los artistas de las canciones en la tabla de alguno de los sitios de last.fm con formato /tag/... y devolverlos en lista. Para eso toma la sopa del sitio con el formato indicado (ej de sitio: "https://www.last.fm/es/tag/acoustic/tracks")
    """
    autoresFilas = sopa.findAll("td", {"class": "chartlist-artist"})
    autores = []
    for f in autoresFilas:
        a = f.find("a")
        autores.append(a.text)
    return(autores)

def linksYTTablaPagTag(sopa):
    """
#Extrae los links de youtube a las canciones en la tabla de alguno de los sitios de last.fm con formato /tag/... y devolverlos en lista. Para eso toma la sopa del sitio con el formato indicado (ej de sitio: "https://www.last.fm/es/tag/acoustic/tracks")
    """
    linksYTFilas = sopa.findAll("td", {"class": "chartlist-play"})
    linksYT = []
    for f in linksYTFilas:
        try:
            a = f.find("a", href=True)['href'] #los a de c/fila que tengan un href, tomar solo el atributo href de a
            linksYT.append(a)
        except:
            continue
    return(linksYT)

def linksPerfilesArtistasTablaPagTag(sopa): 
    """
Extrae los links a los perfiles de artistas de las canciones en la tabla de alguno de los sitios de last.fm con formato /tag/... y devolverlos en lista. Para eso toma la sopa del sitio con el formato indicado (ej de sitio: "https://www.last.fm/es/tag/acoustic/tracks")
    """
    autoresFilas = sopa.findAll("td", {"class": "chartlist-artist"})
    autoresLinks = []
    for f in autoresFilas:
        a = f.find("a", href=True)['href']
        autoresLinks.append("http://www.last.fm"+a)
        #pagVisitar = bajar("http://www.last.fm"+a)
    return(autoresLinks)

def artistasSimilaresAArtistasTablaPagTag(sopa):
    """
Extrae la lista de los 3 artistas similares de las páginas de perfiles de c/u de los artistas en la tabla de alguno de los sitios de last.fm con formato /tag/... y devolverlos en lista. Para eso toma la sopa del sitio con el formato indicado (ej de sitio: "https://www.last.fm/es/tag/acoustic/tracks") Devuelve una lista de listas (1 lista con listas por cada fila de la tabla; en c/u los 3 artistas string, ej [["Abel Pintos", "Shakira", "La Renga"],["uno","dos","tres"]])
    """
    autoresFilas = sopa.findAll("td", {"class": "chartlist-artist"})
    autoresLinks = []
    similaresListaDeLista = []
    for f in autoresFilas:
        a = f.find("a", href=True)['href']
        autoresLinks.append("http://www.last.fm"+a)
        pagVisitar = bajar("http://www.last.fm"+a)
        #Extrae los nombres de los artistas similares
        similaresTitulos = pagVisitar.findAll("h3", {"class": "artist-similar-artists-sidebar-item-name"})
        similares = [] #guarda la lista de los 3 similares a la pag del artista que está visitando
        for f in similaresTitulos:
            a = f.find("a")
            similares.append(a.text)
        similaresListaDeLista.append(similares) #Agrega a la lista de listas de similares para tener juntos todos los de la tabla
    return(similaresListaDeLista)


def crearPaginas(listaGral,modelohtml):
    """
Toma la lista general de lo escrapeado formato ej [("tema","artista","linkvideo",['similar1', 'similar2', 'similar3']),(),()] y un modelo de salida de las pag html que debe crear. Genera una pag html por cada elemento de la lista general, y abre la última generada
    """
    linksAPaginas = ""
    for datos in listaGral:
        linkapag = '<a href="'+datos[1]+datos[0]+'.html">'+datos[0]+' - '+datos[1]+'</a>'
        linksAPaginas += linkapag
    n=0
    for datos in listaGral:
        tema = datos[0].replace("/","-")
        cantante = datos[1].replace("/","-")
        link = '<a href='+datos[2]+'>Escuchar en youtube</a>'
        recomendados = ""
        for reco in datos[3]:
            recomendados = recomendados +  "<br>-"+ reco
        claveBusquedaWiki = cantante.replace(" ","%20")
        n +=1 

            
        with open ("index.html","r") as file:
            content = file.read()
        content = content.replace("{tema}",tema)
        content = content.replace("{cantante}",cantante)
        content = content.replace("{link}",link)
        content = content.replace("{recomendados}",recomendados)
        content = content.replace("{linksAPaginas}",linksAPaginas)
        content = content.replace("{claveBusquedaWiki}",claveBusquedaWiki)
        content = content.replace("{n}",str(n))
        
        with open (cantante+tema+".html", "w") as file:
            file.write(content)
    webbrowser.open(cantante+tema+".html")
 
def armarDireccionPorTagLastFM(index, tags):
    """
    Recibe un index  y la lista de tags existentes, y si está en la lista devuelve la url que va a la lista de tracks en las last fm de ese tag; sino devuelve None
    """ 
    if index <= len(tags)-1:
        return "https://www.last.fm/es/tag/"+tags[index]+"/tracks"
    else:
        return None


def pedirNumeroEntero():
 
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Introduce un numero de la lista de opciones: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero de la lista de opciones')
     
    return num

def guardarEnCSV(listaaguardar):
    with open("datos.txt", "w") as f:
        writer = csv.writer(f)
        for e in listaaguardar:
            writer.writerow(e)



if __name__ == "__main__":
    
    tags = ["electronic","rock","hip-hop", "indie", "jazz", "reggae", "british", "punk", "80s", "dance", "acoustic", "rnb", "hardore", "country", "blues", "alternative", "classical", "rap", "country", "metal"]
    
    salir = False
    opcion = 0
    
    while not salir:
 
        print ("1. Scrapear datos de www.last.fm según tu tipo de música preferida, generar sitios web y guardar scrapeo en csv")
        print ("2. Salir")
         
        print ("Elige una opcion")
     
        opcion = pedirNumeroEntero()
     
        if opcion == 1:
            print("Seleccione un tipo de música correspondiente a los tags de Last FM")
            for tag in tags:
                print (" -"+str(tags.index(tag))+". "+tag)
            print (str(len(tags))+". Volver al menú principal")
            print (str(len(tags)+1)+". Salir")
             
            print ("Elige una opcion")
         
            opcion = pedirNumeroEntero()
         
            if (opcion >= 0) and (opcion <= len(tags)-1):
                
                #Ejecuto escrapeado y armado de paginas
                dirl = armarDireccionPorTagLastFM(opcion, tags)
                print("bajando sitio: " + dirl)
                #dir1 = "https://www.last.fm/es/tag/acoustic/tracks"
                sopa = bajar(dirl)

                print("Scrapeando lista de canciones... ")
                canciones = cancionesTablaPagTag(sopa)
                print("Scrapeando lista de artistas... ")
                cantantes = artistasTablaPagTag(sopa)
                print("Scrapeando lista de links a youtube... ")                
                linksTemas = linksYTTablaPagTag(sopa)
                print("Scrapeando artistas similares... aguarde, esto puede tomar algún tiempo")
                similares = artistasSimilaresAArtistasTablaPagTag(sopa)
                

                rows = zip(canciones, cantantes, linksTemas, similares)
                listageneral = []
                
                for row in rows:
                    #print(row)
                    listageneral.append(row)
                
                print("Guardando en csv.")                
                guardarEnCSV(listageneral)
                print("Generando páginas html.")  
                crearPaginas(listageneral,"index.html")


            elif opcion == len(tags):
                continue
            elif opcion == len(tags)+1:
                salir = True
            else:
                print ("Introduce un numero entre 1 y "+ str(len(tags)+1))          
        elif opcion == 2:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 2")
    
 

    """ 
    #Data sample guardado de un scrapeo anterior
    listageneral = [("I'm Yours", 'Jason Mraz', 'https://www.youtube.com/watch?v=EkHTsc9PU2A', ['Gavin DeGraw', 'James Morrison', 'John Mayer']), ('Hurt', 'Johnny Cash', 'https://www.youtube.com/watch?v=8AHCfZTRGiI', ['Johnny Cash & June Carter', 'The Highwaymen', 'Johnny Cash & June Carter Cash']), ('Hey There Delilah', "Plain White T's", 'https://www.youtube.com/watch?v=h_m-BjrxmgI', ['The All-American Rejects', 'Boys Like Girls', 'We the Kings']), ('Better Together', 'Jack Johnson', 'https://www.youtube.com/watch?v=seZMOTGCDag', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('I Will Follow You Into The Dark', 'Death Cab for Cutie', 'https://www.youtube.com/watch?v=NDHY1D0tKRA', ['Ben Gibbard', 'The Postal Service', 'The Shins']), ('Hallelujah', 'Jeff Buckley', 'https://www.youtube.com/watch?v=y8AWFf7EAc4', ['Tim Buckley', 'Elliott Smith', 'Radiohead']), ('Cannonball', 'Damien Rice', 'https://www.youtube.com/watch?v=3yqM--IMkX4', ['Glen Hansard', 'Lisa Hannigan', 'Iron & Wine']), ('Tears in Heaven', 'Eric Clapton', 'https://www.youtube.com/watch?v=JxPj3GAYYZ0', ['Derek and the Dominos', 'J.J. Cale & Eric Clapton', 'B.B. King & Eric Clapton']), ('Charlie Conscience (feat. MMAIO)', 'Juzhin', 'https://www.youtube.com/watch?v=iOcc5eEtkTM', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Railways', 'Juzhin', 'https://www.youtube.com/watch?v=1GezTDIb52Q', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Coming Down', 'Juzhin', 'https://www.youtube.com/watch?v=iOcc5eEtkTM', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Tupona', 'Juzhin', 'https://www.youtube.com/watch?v=RGv4PRqYqK4', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Sakhalin', 'Juzhin', 'https://www.youtube.com/watch?v=Mnd0j8QwQI4', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Heartbeats', 'José González', 'https://www.youtube.com/watch?v=TOsRkcV8pCk', ['Junip', 'Ben Howard', 'Alexi Murdoch']), ('Sitting, Waiting, Wishing', 'Jack Johnson', 'https://www.youtube.com/watch?v=IhTvifGShw4', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('3 Simple Minutes', 'Juzhin', 'https://www.youtube.com/watch?v=iOcc5eEtkTM', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Such Great Heights', 'Iron & Wine', 'https://www.youtube.com/watch?v=tCYWymG9fSs', ['Iron & Wine and Calexico', 'M. Ward', 'The Tallest Man on Earth']), ("The Blower's Daughter", 'Damien Rice', 'https://www.youtube.com/watch?v=5YXVMCHG-Nk', ['Glen Hansard', 'Lisa Hannigan', 'Iron & Wine']), ('Mad World', 'Gary Jules', 'https://www.youtube.com/watch?v=ZUtAe5PUKtE', ['Five for Fighting', 'Joshua Radin', 'David Gray']), ('Lost Sense', 'Juzhin', 'https://www.youtube.com/watch?v=iOcc5eEtkTM', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Collide', 'Howie Day', 'https://www.youtube.com/watch?v=ca9ub9rpNK4', ['Five for Fighting', 'Matt Nathanson', 'Lifehouse']), ('More Than Words', 'Extreme', 'https://www.youtube.com/watch?v=UrIiLvg58SY', ['Mr. Big', 'David Lee Roth', 'Winger']), ('Banana Pancakes', 'Jack Johnson', 'https://www.youtube.com/watch?v=OkyrIRyrRdY', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('9 Crimes', 'Damien Rice', 'https://www.youtube.com/watch?v=cgqOSCgc8xc', ['Glen Hansard', 'Lisa Hannigan', 'Iron & Wine']), ('This Is the Life', 'Amy Macdonald', 'https://www.youtube.com/watch?v=iRYvuS9OxdA', ['Katzenjammer', "Dolores O'Riordan", 'KT Tunstall']), ('Wonderful', 'Juzhin', 'https://www.youtube.com/watch?v=APW_PueCbds', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Flunk - Down (Juzhin Remix)', 'Juzhin', 'https://www.youtube.com/watch?v=AWGqoCNbsvM', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Bubbly', 'Colbie Caillat', 'https://www.youtube.com/watch?v=Nd-A-iiPoLg', ['Sara Bareilles', 'Christina Perri', 'Ingrid Michaelson']), ('Naked As We Came', 'Iron & Wine', 'https://www.youtube.com/watch?v=iOcc5eEtkTM', ['Iron & Wine and Calexico', 'M. Ward', 'The Tallest Man on Earth']), ('Squat', 'Juzhin', 'https://www.youtube.com/watch?v=Dz5s5C6sAt0', ['Sequence Theory Project', 'Azoora feat. graciellita', 'Elenika']), ('Skinny Love', 'Bon Iver', 'https://www.youtube.com/watch?v=zwFS69nA-1w', ['Volcano Choir', 'Justin Vernon', 'Sufjan Stevens']), ('First Day of My Life', 'Bright Eyes', 'https://www.youtube.com/watch?v=BblV6AQsd2s', ['Conor Oberst', 'Conor Oberst and the Mystic Valley Band', 'Desaparecidos']), ('Swing Life Away', 'Rise Against', 'https://www.youtube.com/watch?v=N5EnGwXV_Pg', ['Sum 41', 'Billy Talent', 'Anti-Flag']), ('Your Body Is a Wonderland', 'John Mayer', 'https://www.youtube.com/watch?v=ZduDvIBu3EU', ['John Mayer Trio', 'Jason Mraz', 'Jack Johnson']), ('Volcano', 'Damien Rice', 'https://www.youtube.com/watch?v=7_RZLAxsa8Q', ['Glen Hansard', 'Lisa Hannigan', 'Iron & Wine']), ('Seaside', 'The Kooks', 'https://www.youtube.com/watch?v=dRPwFAoQwxc', ['The Fratellis', 'The Wombats', 'The Pigeon Detectives']), ('Delicate', 'Damien Rice', 'https://www.youtube.com/watch?v=cG8kBsjfVp8', ['Glen Hansard', 'Lisa Hannigan', 'Iron & Wine']), ('Heartbeats', 'José González', 'https://www.youtube.com/watch?v=9AZVXorIZNs', ['Junip', 'Ben Howard', 'Alexi Murdoch']), ('Good People', 'Jack Johnson', 'https://www.youtube.com/watch?v=WOxE7IRizjI', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('Breakdown', 'Jack Johnson', 'https://www.youtube.com/watch?v=Inlac4FyhD8', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('Misread', 'Kings of Convenience', 'https://www.youtube.com/watch?v=irq959oNVww', ['Erlend Øye', 'The Whitest Boy Alive', 'José González']), ('Wonderwall', 'Ryan Adams', 'https://www.youtube.com/watch?v=MMFj8uDubsE', ['Ryan Adams & The Cardinals', 'Whiskeytown', 'Jason Isbell']), ('Pink Moon', 'Nick Drake', 'https://www.youtube.com/watch?v=VUf7w4e2sSE', ['Elliott Smith', 'Tim Buckley', 'Jackson C. Frank']), ("Blowin' in the Wind", 'Bob Dylan', 'https://www.youtube.com/watch?v=AtkBgbQxBs0', ['Bob Dylan and The Band', 'Bob Dylan & Johnny Cash', 'The Band']), ('Flake', 'Jack Johnson', 'https://www.youtube.com/watch?v=oBIxScJ5rlY', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('Never Know', 'Jack Johnson', 'https://www.youtube.com/watch?v=_DboMAghWcA', ['Donavon Frankenreiter', 'Ben Harper', 'Matt Costa']), ('Waiting on the World to Change', 'John Mayer', 'https://www.youtube.com/watch?v=LuQrLsTUcN0', ['John Mayer Trio', 'Jason Mraz', 'Jack Johnson']), ('Hero of War', 'Rise Against', 'https://www.youtube.com/watch?v=dqUdI4AIDF0', ['Sum 41', 'Billy Talent', 'Anti-Flag'])]
    """



"""
Fuentes:
http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
https://stackoverflow.com/questions/5815747/beautifulsoup-getting-href
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://www.youtube.com/watch?v=4W7HeJvAaD0&ab_channel=iTecnoGalaxy
https://python-para-impacientes.blogspot.com/2015/11/abrir-paginas-web-en-un-navegador-con.html
https://www.discoduroderoer.es/crear-un-menu-de-opciones-en-consola-en-python/
"""