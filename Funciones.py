from requests import post, get
from functools import reduce
from Clases import Artista, Cancion
import base64
import json

#FUNCIONES PARA EL PROCEDURAL

def obtener_token(id_cliente, id_secret_cliente): #con las credenciales se obtiene el token para la usar la API
    autenti_string = id_cliente + ":" + id_secret_cliente      #toma las credenciales y las junta 
    autenti_bytes = autenti_string.encode("utf-8")          #se pasa a una representación en bytes
    autenti_base64 = str(base64.b64encode(autenti_bytes), "utf-8") #codifica los bytes y convierte el resultado en un string
    
    url = "https://accounts.spotify.com/api/token" #url para obtener el token


    headerss =  {"Authorization": "Basic " + autenti_base64,            #configura los encabezados de la solicitud, incluyendo la autorizacion dada por autenti_base64
                "Content-Type": "application/x-www-form-urlencoded"}    #indica el tipo de contenido de la solicitud
    
    data = {"grant_type": "client_credentials"} #se especifica el tipo de autentificación para enviar la solicitud del token
    resultado = post(url, headers = headerss, data = data) #se hace envia las credenciales y el tipo de autentificación con el post (forma de enviar datos al servidor)
    resultado_json = json.loads(resultado.content) #se convierte el resultado json a un diccionario (el token en este caso)

    token = resultado_json["access_token"] #con la clave "access_token" se accede al valor del token
    return token

def obtener_header(token):
    return {"Authorization": "Bearer " + token} #hace los headers para los siguientes solicitudes que se necesiten (es la autorización que tenemos)

def buscar_playlist(token, nombre_playlist):
    url = "https://api.spotify.com/v1/search" #url para buscar la playlist

    headerss = obtener_header(token) #se obtiene el header de acuerdo al token que tenemos

    filtro = (f"?q={nombre_playlist}&type=playlist&limit=1") #según la documentación de la API, para buscar un dato se usa el siguiente formato en la url

    buscador = url + filtro #guarda la url para la busqueda
    resultado = get(buscador, headers = headerss) #se piden los datos a la API para obtener el resultado de lo buscado
    resultado_json = json.loads(resultado.content)["playlists"]["items"]  #se convierte el resultado json a un diccionario y accedede a los datos de playlist para entrar a items

    return (resultado_json[0]) #retorna la primera busqueda 

def fun_artista(token, id_artista):
    url = f"https://api.spotify.com/v1/artists/{id_artista}" #url para obtener los datos del artista
    headerss = obtener_header(token) #se obtiene el header

    resultado = get(url, headers = headerss) #se piden los datos a la API para obtener el resultado de lo buscado
    resultado_json = json.loads(resultado.content) #se convierte el resultado json a un diccionario
    return resultado_json #retorna los datos del artista

def playlist(token, id_playlist):
    url = f"https://api.spotify.com/v1/playlists/{id_playlist}" #url para obtener los datos de una playlist
    headerss = obtener_header(token) #se obtiene el header

    resultado = get(url, headers = headerss) #se piden los datos a la API para obtener el resultado de lo buscado
    resultado_json = json.loads(resultado.content) #se convierte el resultado json a un diccionario
    return resultado_json #retorna la playlist

def rellenador_datos(cantidad_de_canciones, playlist, token):
    lista_canciones = []
    lista_artistas = []

    for i in range(cantidad_de_canciones-1): #se recorren las canciones de la playlist
        artistas_cancion = []
        NroDeArtsDeLaCancion = len(playlist["tracks"]["items"][i]["track"]["artists"])

        for art in range(NroDeArtsDeLaCancion): #se recorren los artistas de las canciones

            id_artista = playlist["tracks"]["items"][i]["track"]["artists"][art]["id"] #se selecciona la canción i y se obtiene el id 
                                                                                          #de uno de sus artistas
            
            arti_momento = fun_artista(token, id_artista) #se busca al artista por su id para tener su información

            nombre_artista = playlist["tracks"]["items"][i]["track"]["artists"][art]["name"] #se obtiene el nombre del artista

            artistas_cancion.append(nombre_artista) #a la lista de artistas de esa canción se agrega ese nombre

            #a su vez, se crea el objeto del artista en particular para almacenar sus datos
            artista = Artista(arti_momento["followers"]["total"], arti_momento["genres"], nombre_artista,arti_momento["popularity"], id_artista, None) 
            #la frecuencia de cuantas veces sale en la playlist el artista en la playlist se almacena de a poco (por eso parte con 0)
            

            frec_actual = frecuenciador(artista, lista_artistas) #se ve si el artista ya fue visto en esta playlist

            if frec_actual == -1: #retorna -1 (la función frecuenciador) en caso de que no haya estado, y por ende se agrega a la lista de objetos artistas con frec = 1
                artista.frecuencia = 1 
                lista_artistas.append(artista)
            else: 
                lista_artistas[frec_actual[0]].frecuencia = frec_actual[1] #en caso de haber estado antes, se accede a la posición de ese artista y +1 a su frecuencia

        #termina el ciclo de los artistas de la canción y se agregan los datos particulares de la canción 
        cancion = Cancion(playlist["tracks"]["items"][i]["track"]["id"],
                          playlist["tracks"]["items"][i]["track"]["name"],
                          artistas_cancion,
                          playlist["tracks"]["items"][i]["track"]["album"]["name"],
                          playlist["tracks"]["items"][i]["track"]["duration_ms"],
                          playlist["tracks"]["items"][i]["track"]["explicit"],
                          playlist["tracks"]["items"][i]["track"]["popularity"],
                          playlist["tracks"]["items"][i]["track"]["preview_url"])
        
        lista_canciones.append(cancion) #se agrega la canción a una lista de objetos canciones
    
    return lista_canciones, lista_artistas

#una función que se hizo para una clase
def islistadestr(entrada):
    return isinstance(entrada, list) and all(isinstance(elemento, str) for elemento in entrada)


#FUNCIONES PARA EL FUNCIONAL

#funcional que rellena las frecuencias de los artistas para luego saber el que tiene mayor frecuencia
def frecuenciador(objeto, lista):  
    """ proceso de forma no funcional --> para entender nada más
    lista_con_indexs = list(enumerate(lista))
    
    lista_filtrada = list(filter(lambda x: x[1].id == objeto.id, lista_con_indexs)) --> saca una lista con los objetos con el mismo id
    
    resultado = reduce(lambda acc, x: (x[0], x[1].frecuencia + 1) if acc is None else acc, lista_filtrada, None) --> toma el primer objeto coincidente y aumenta su frecuencia en 1
    
    return result if resultado is not None else -1 --> Si no se encontró ningún objeto, devuelve -1
    """
    return reduce(
        lambda acum, x: (x[0], x[1].frecuencia + 1) if acum is None else acum, 
        list(filter(lambda x: x[1].id == objeto.id, list(enumerate(lista)))), 
        None
        ) if reduce(
            lambda acum, x: (x[0], x[1].frecuencia + 1) if acum is None else acum,
            list(filter(lambda x: x[1].id == objeto.id, list(enumerate(lista)))), 
            None) is not None else -1

def artistamasfrecuente(lista):
     return max(lista, key = lambda y: y.frecuencia) #retorna el objeto artista

def proporcionExplicitas(lista):
    return len(list(filter(lambda x: x.explicita == True, lista)))/len(lista), len(list(filter(lambda x: x.explicita == False, lista)))/len(lista)

def masmenospopulares(listaArt, listaCan):
    #retorna los objetos artistas y cancion que tienen dichas características
    return max(listaArt, key = lambda y: y.popularidad), min(listaArt, key = lambda x: x.popularidad), max(listaCan, key = lambda a: a.popularidad), min(listaCan, key = lambda b: b.popularidad)
       
def promedio_duracion_can(lista):
    """ proceso no de forma totalmente funcional --> para entender nada más
    duraciones = list(map(lambda x: x.duracion, lista))

    media = reduce(lambda acum, duracion: acum + duracion, duraciones) / len(duraciones)
    """
    return reduce(lambda acum, duracion: acum + duracion, list(map(lambda x: x.duracion, lista))) / len(list(map(lambda x: x.duracion, lista)))

def desvi_popularidad(lista):
    """ proceso de forma no funcional --> para entender nada más

    popularidades = list(map(lambda x: x.popularidad, lista))

    media = reduce(lambda acc, popularidad: acc + popularidad, popularidades) / len(popularidades)

    suma_cuadrados_diferencidos = reduce(lambda acc, popularidad: acc + (popularidad - media) ** 2, popularidades, 0)

    desviacion_estandar = ((suma_cuadrados_diferencidos / (len(popularidades) - 1)))**(0.5)
    """
    return ((reduce(lambda acum, popularidad: acum + (popularidad - reduce(lambda acum, popularidad: acum + popularidad,
                                                                                  list(map(lambda x: x.popularidad, lista))) / len(list(map(lambda x: x.popularidad, lista)))) ** 2, 
                                                                                  list(map(lambda x: x.popularidad, lista)), 0) / (len(list(map(lambda x: x.popularidad, lista))) - 1))) ** (0.5)
