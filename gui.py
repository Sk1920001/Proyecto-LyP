import tkinter as tk
from tkinter import ttk
from Funciones import *
from Clases import *


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
        self.label = ttk.Label(self.root, text="Ingrese el nombre de la playlist")
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
        self.__result_label = ttk.Label(self.root, text=f"Resultados obtenidos para: {self.__playlist_filter}")
        self.__result_label.pack(pady=10)
        
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
        self.__playlist_name=playlistPro["name"]

        cantidad_canciones = len(playlistPro["tracks"]["items"]) #en la playlist se accede al apartado tracks y luego se ve el total de canciones

        self.__songs,self.__artist = rellenador_datos(cantidad_canciones, playlistPro, tok)
        art_popular, art_nopopular, can_popular, can_nopopular = masmenospopulares(self.__artist, self.__songs)
        desvi_popularidad_art = round(desvi_popularidad(self.__artist),2) 
        desvi_popularidad_can = round(desvi_popularidad(self.__songs),2)
        prop_exp, prop_noexp = proporcionExplicitas(self.__songs)
        
        self.__metrics = [
            f"Nombre de la playlist: {self.__playlist_name}",
            f"Artista más frecuente: {artistamasfrecuente(self.__artist).nombre}",
            f"Promedio duración por canción: {promedio_duracion_can(self.__songs)}",
            f"Proporción de canciones explícitas: {prop_exp}",
            f"Artista más popular: {art_popular.nombre}, con una popularidad de: {art_popular.popularidad}",
            f"Canción más polular: {can_popular.nombre}, con una popularidad de: {can_popular.popularidad}",
            f"Canción menos popular: {can_nopopular.nombre}con una popularidad de: {can_popular.popularidad}",
            f"Desviación estándar de la popularidad de los artistas: {desvi_popularidad_art}",
            f"Desviación estándar de la popularidad de las canciones: {desvi_popularidad_can}"

        ]

        for value in self.__metrics:
            value_label = ttk.Label(self.root, text=value)
            value_label.pack()
        
        self.load_songs()

        # Botón de regresar
        self.button_frame=ttk.Frame(self.root)
        self.button_frame.pack()
        self.back_button = ttk.Button(self.button_frame, text="Regresar", command=self.pre_screen)
        self.game_button = ttk.Button(self.button_frame, text="Jugar", command=self.play)
        self.back_button.pack(pady=10,side=tk.LEFT)
        self.game_button.pack(pady=10, padx=10,side=tk.LEFT)


    def load_songs(self):
        for song in self.__songs:
            self.tree.insert("", tk.END, values=(song.nombre, song.album, song.duracion, song.explicita))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def play(self):
        screen=pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
        pygame.font.init()
        pygame.display.set_caption("Juegito")    
        player = Player("El master del juego")
        game = GameScreen(player)
        game.start(self.__songs)
        buttons = [game.button1, game.button2]
        clock=pygame.time.Clock()
        elapsed_time = 0
        
        running = True

        while running:
            
            if(len(game.used_songs) == len(game.playlist_songs)-3):
                pygame.quit()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  #botón izq del mouse
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.click(game.current_song.nombre) == True:
                                    player.score += 1
                                    game.changeButtons("Correct",screen)
                                    buttons = [game.button1, game.button2]
                                    elapsed_time = 0
                                    continue
                                else:
                                    game.changeButtons("Incorrect",screen)
                                    buttons = [game.button1, game.button2]
                                    elapsed_time = 0
                                    continue

            #actualiza el estado de los botones
            for button in buttons:
                button.update()
                
            
            elapsed_time += clock.tick(60) / 1000  #Convierte los milisegundos a segundos (limita a 60 frames por segundo y calcula el paso de un frame)
            if elapsed_time >= 10:
                game.changeButtons("Incorrect",screen)
                buttons = [game.button1, game.button2]
                elapsed_time = 0

            #se dibuja en la pantalla
            screen.fill(Constants.WHITE)
            game.drawButtons(screen)
            game.drawscore(screen)
            pygame.display.flip() #no lo pongo dentro de la clase ya que parpadearian los objetos, ya que estaría haciendo flip dos veces
    
        pygame.quit()

    

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()