import tkinter as tk
from tkinter import ttk
from Funciones import *
from Clases import Constants

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto LyP")
        self.__playlist_filter = ""
        self.__search_message = ""
        self.__songs = None
        self.__artist = None
        self.__playlist_name = None  
        self.__metrics = None 

        # Pantalla previa
        self.pre_screen()

    def pre_screen(self):
        self.clear_screen()
        
        # Etiqueta y campo de texto
        self.label = ttk.Label(self.root, text="Ingrese el nombre de la playlist:")
        self.label.pack(pady=10)
        
        self.entry = ttk.Entry(self.root)
        self.entry.pack(pady=10)
        
        # Botón de enviar
        self.submit_button = ttk.Button(self.root, text="Enviar", command=self.show_results)
        self.submit_button.pack(pady=10)

    def show_results(self):
        self.__playlist_filter= self.entry.get()
        
        self.clear_screen()

        # Mostrar nombre de usuario
        self.greeting_label = ttk.Label(self.root, text=f"Resultados obtenidos para: {self.__playlist_filter}")
        self.greeting_label.pack(pady=10)
        
        # Crear un marco para el árbol de inventario
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Crear un árbol (Treeview) para mostrar el inventario
        self.tree = ttk.Treeview(self.frame, columns=("Nombre", "Album", "Duracion","Explicita"), show='headings')
        self.tree.heading("Nombre", text="Nombre canción")
        self.tree.heading("Album", text="Álbum")
        self.tree.heading("Duracion", text="Duración (ms)")
        self.tree.heading("Explicita", text="Explícita")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Agregar algunos elementos al inventario
        tok = obtener_token(Constants().ID_CLIENTE, Constants().SECRET_CLIENTE)

        nombre_a_buscar = self.__playlist_filter

        id_playlist = buscar_playlist(tok, nombre_a_buscar)["id"] #se busca una playlist y se selecciona su id
        playlistPro = playlist(tok, id_playlist) #se busca la playlist según el id
        print(playlistPro)
        self.__playlist_name=playlistPro["name"]
        cantidad_canciones = playlistPro["tracks"]["total"] #en la playlist se accede al apartado tracks y luego se ve el total de canciones
        print(playlistPro["tracks"]["total"]) #bug que solucionar

        self.__songs,self.__artist = rellenador_datos(cantidad_canciones, playlistPro, tok)

        self.__metrics = [
            f"Nombre: {self.__playlist_name}",
            f"Artista más frecuente: {artistamasfrecuente(self.__artist).nombre}",
            f"Promedio duración por canción: {promedio_duracion_can(self.__songs)}"
        ]

        for value in self.__metrics:
            value_label = ttk.Label(self.root, text=value)
            value_label.pack()
        
        self.load_songs()

        # Botón de regresar
        self.back_button = ttk.Button(self.root, text="Regresar", command=self.pre_screen)
        self.back_button.pack(pady=10)

    def load_songs(self):
        for song in self.__songs:
            self.tree.insert("", tk.END, values=(song.nombre, song.album, song.duracion, song.explicita))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()