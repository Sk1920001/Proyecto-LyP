from requests import post, get
import base64
import json



def credenciales():
    cliente_id = "74c0383b8305467db74ef28e3e8046f2"
    cliente_secret = "331c151f6ad749a2b36d81ef97a69360"
    return cliente_id, cliente_secret

def obtener_token():
    id_cliente = credenciales()[0]
    secret_cliente = credenciales()[1]

    autenti_string = id_cliente + ":" + secret_cliente
    autenti_bytes = autenti_string.encode("utf-8")
    autenti_base64 = str(base64.b64encode(autenti_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"

    headerss =  {"Authorization": "Basic " + autenti_base64,
                "Content-Type": "application/x-www-form-urlencoded"}
    
    data = {"grant_type": "client_credentials"}
    resultado = post(url, headers = headerss, data = data)
    resultado_json = json.loads(resultado.content)

    token = resultado_json["access_token"]
    return token

def obtener_header(token):
    return {"Authorization": "Bearer " + token}





def buscar_playlist(token, nombre_playlist):
    url = "https://api.spotify.com/v1/search"

    headerss = obtener_header(token)
    filtro = (f"?q={nombre_playlist}&type=playlist&limit=1")

    buscador = url + filtro
    resultado = get(buscador, headers = headerss)
    resultado_json = json.loads(resultado.content)["playlists"]["items"]

    return (resultado_json[0])



def playlist(token, id_playlist):
    url = f"https://api.spotify.com/v1/playlists/{id_playlist}"
    headerss = obtener_header(token)

    resultado = get(url, headers = headerss)
    resultado_json = json.loads(resultado.content)
    return resultado_json




