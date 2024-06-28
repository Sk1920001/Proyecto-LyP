from Funciones import *
from Clases import Constants

def main():
    tok = obtener_token(Constants().ID_CLIENTE, Constants().SECRET_CLIENTE)

    nombre_a_buscar = "Top 50: Global"

    id_playlist = buscar_playlist(tok, nombre_a_buscar)["id"] #se busca una playlist y se selecciona su id
    playlistPro = playlist(tok, id_playlist) #se busca la playlist según el id

    cantidad_canciones = playlistPro["tracks"]["total"] #en la playlist se accede al apartado tracks y luego se ve el total de canciones
    
    canciones, artistas = rellenador_datos(cantidad_canciones, playlistPro, tok)

    art_frecuente = artistamasfrecuente(artistas)
    
    prop_exp, prop_noexp = proporcionExplicitas(canciones)

    art_popular, art_nopopular, can_popular, can_nopopular = masmenospopulares(artistas, canciones)

    desvi_popularidad_art = desvi_popularidad(artistas) 
    desvi_popularidad_can = desvi_popularidad(canciones)

    prom_dur_can = promedio_duracion_can(canciones)

    print(f"el artista más frecuente en la playlist es {art_frecuente.nombre} con una frecuencia de {art_frecuente.frecuencia} canciones" )
    print(f"la proporción de canciones explicitas en la playlist es de {prop_exp}, de no explicitas es {prop_noexp}")
    print(f"el artista más popular según spotify es {art_popular.nombre} con un valor de {art_popular.popularidad}, mientras que el menos popular es {art_nopopular.nombre} con un valor de {art_nopopular.popularidad}")
    print(f"la canción más popular de la playlist según Spotify es {can_popular.nombre} con un valor de {can_popular.popularidad}, esta canción pertenece a {can_popular.artistas}")
    print(f"la canción menos popular de la playlist según Spotify es {can_nopopular.nombre} con un valor de {can_nopopular.popularidad}, esta canción pertenece a {can_nopopular.artistas}")
    print(f"la desviación estandar de la popularidad de los artistas de la playlist es {desvi_popularidad_art}")
    print(f"la desviación estandar de la popularidad de las canciones de la playlist es {desvi_popularidad_can}")
    print(f"el promedio de la duración de las canciones de la playlist es {prom_dur_can} ms")


if __name__ == "__main__":
    main()
    
