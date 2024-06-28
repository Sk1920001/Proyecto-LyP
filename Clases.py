from Funciones import *
from io import BytesIO

import pygame.display
import pygame
import random
import time
import requests

class Constants:
    ID_CLIENTE =  "74c0383b8305467db74ef28e3e8046f2" 
    SECRET_CLIENTE = "331c151f6ad749a2b36d81ef97a69360"
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0,255,255)
    LIGHT_GRAY = (200, 200, 200)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class ObjetoMusical:
    def __init__(self, id, nombre, popularidad):
        self.__id = id
        self.__nombre = nombre
        self.__popularidad = popularidad

    #getters

    @property 
    def nombre(self):
        return self.__nombre
    
    @property 
    def popularidad(self):
        return self.__popularidad
    
    @property 
    def id(self):
        return self.__id
    
    #setters

    @nombre.setter
    def nombre(self, nombre_nuevo):
        if isinstance(nombre_nuevo, str):
            self.__nombre = nombre_nuevo
        else:
            raise ValueError("el nombre debe ser un string")

    @popularidad.setter
    def popularidad(self, popularidad_nuevo):
        if isinstance(popularidad_nuevo, int) and popularidad_nuevo >= 0:
            self.__popularidad = popularidad_nuevo
        else:
            raise ValueError("la popularidad debe ser un int igual a 0 o positivo")
        

    @id.setter
    def id(self, id_nuevo):
        if isinstance(id_nuevo, str):
            self.__id = id_nuevo
        else:
            raise ValueError("el id debe ser un string")
        
class Artista(ObjetoMusical):
    def __init__(self, cant_seguidores, genero, nombre, popularidad, id, frecuencia):
        super().__init__(id, nombre, popularidad)
        self.__cant_seguidores = cant_seguidores
        self.__genero = genero
        self.__frecuencia = frecuencia

    #getters

    @property 
    def cant_seguidores(self):
        return self.__cant_seguidores
    
    @property 
    def genero(self):
        return self.__genero
    
    @property
    def frecuencia(self):
        return self.__frecuencia
    
    #setters

    @cant_seguidores.setter
    def cant_seguidores(self, cant_seguidores_nuevo):
        if isinstance(cant_seguidores_nuevo, int) and cant_seguidores_nuevo >= 0:
            self.__cant_seguidores = cant_seguidores_nuevo
        else:
            raise ValueError("la cantidad de seguidores debe ser un int igual a 0 o positivo")

    @genero.setter
    def genero(self, genero_nuevo):
        if islistadestr(genero_nuevo) == True:
            self.__genero = genero_nuevo
        else:
            raise ValueError("el genero del artista debe ser una lista de strings")
    
    @frecuencia.setter
    def frecuencia(self, frecuencia_nueva):
        if isinstance(frecuencia_nueva, int) and frecuencia_nueva >= 0:
            self.__frecuencia = frecuencia_nueva
        else:
            raise ValueError("la frecuencia debe ser un int igual a 0 o positivo")
    
class Cancion(ObjetoMusical):
    def __init__(self, id, nombre, artistas, album, duracion, explicita, popularidad, preview_url):
        super().__init__(id, nombre, popularidad)
        self.__artistas = artistas 
        self.__album = album 
        self.__duracion = duracion
        self.__explicita = explicita
        self.__preview_url = preview_url

    #getters

    @property
    def artistas(self):
        return self.__artistas
    
    @property
    def album(self):
        return self.__album
    
    @property
    def duracion(self):
        return self.__duracion
    
    @property
    def explicita(self):
        return self.__explicita
    
    @property
    def preview_url(self):
        return self.__preview_url
    

    #setters

    @album.setter
    def album(self, album_nuevo):
        if isinstance(album_nuevo, str):
            self.__album = album_nuevo
        else: 
            raise ValueError("el nombre del album debe ser un string")
    
    @duracion.setter
    def duracion(self, duracion_nueva):
        if isinstance(duracion_nueva, int) and duracion_nueva >= 0:
            self.__duracion = duracion_nueva
        else:
            raise ValueError("la duracion de la cancion en milisegundos debe ser un int mayor o igual a 0")
    
    @explicita.setter
    def explicita(self, explicita_nueva):
        if isinstance(explicita_nueva, bool):
            self.__explicita = explicita_nueva
        else: 
            raise ValueError("la categorización de si una cancion es explicita o no, se debe hacer con True o False respectivamente")
    
    @preview_url.setter
    def preview_url(self, preview_url_nueva):
        if isinstance(preview_url_nueva, str) or preview_url_nueva == None:
            self.__preview_url = preview_url_nueva
        else:
            raise ValueError("la url del preview debe ser dada con un string o puede ser None")
        


"""
Clases para el juego (usan algunas otras constantes de la clase constantes):
"""
#creo que esta lista
class Player:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__score = 0

    @property
    def score(self):
        return self.__score
    
    @property
    def nombre(self):
        return self.__nombre
    
    @score.setter
    def score(self, score_nueva):
        if isinstance(score_nueva, int) and score_nueva >= 0:
            self.__score = score_nueva
        else:
            raise ValueError("el score debe ser un int igual a 0 o positivo")
        
    @nombre.setter
    def nombre(self, nombre_nueva):
        if isinstance(nombre_nueva, str):
            self.__nombre = nombre_nueva
        else:
            raise ValueError("el nombre debe ser un String")

#ver tema del encapsulamiento y de los setters y getters, esta compleja la cosa, al descomentar me da error, no se pq
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.font = font
    


    #métodos
    
    def draw(self, screen):
        # Dibuja el boton, ve si esta el puntero encima, utiliza ese color, en caso contrario, utiliza el otro color(normal)
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        
        # Carga el texto
        text_surf = self.font.render(self.text, True, Constants.BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect) #(texto,posicion)

    def update(self):
        # Ve si el raton esta encima
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def click(self,song):
        if self.text == song:
            return True
        else:
            return False

class GameScreen:
    def __init__(self, player):
        self.__button1 = None
        self.__button2 = None
        self.__playlist_songs = []
        self.__used_songs = []
        self.__current_song = None
        self.__mixer = None
        self.__player = player
        self.__font = pygame.font.Font(None, 25)

    #getters
    @property
    def button1(self):
        return self.__button1
    
    @property
    def button2(self):
        return self.__button2
    
    @property
    def current_song(self):
        return self.__current_song
    
    @property
    def playlist_songs(self):
        return self.__playlist_songs
    
    @property
    def used_songs(self):
        return self.__used_songs
    
    @property
    def mixer(self):
        return self.__mixer
    
    @property
    def player(self):
        return self.__player
    
    @property
    def font(self):
        return self.__font

    #setters
    
    @button1.setter
    def button1(self, button1_nueva):
        self.__button1 = button1_nueva

    @button2.setter
    def button2(self, button2_nueva):
        self.__button2 = button2_nueva

    @current_song.setter
    def current_song(self, current_song_nueva):
        self.__current_song = current_song_nueva
    
    @playlist_songs.setter
    def playlist_songs(self, playlist_songs_nueva):
        self.__playlist_songs = playlist_songs_nueva

    @used_songs.setter
    def used_songs(self, used_songs_nueva):
        self.__used_songs = used_songs_nueva

    @mixer.setter
    def mixer(self, mixer_nueva):
        self.__mixer = mixer_nueva

    @player.setter
    def player(self, player_nueva):
        self.__player = player_nueva

    @font.setter
    def fonr(self, font_nueva):
        self.__font = font_nueva

    #métodos

    def __setPlaylistSongs(self,playlist):
        
        for song in playlist:
            if(song.preview_url == None):
                continue
            self.__playlist_songs.append(song)
            print(song.nombre)
    
        

    def __setCurrentSong(self):
        if len(self.__playlist_songs) == 0:
            raise ValueError("Playlist cannot be empty")
        not_used_songs=[song for song in self.__playlist_songs if song.nombre not in self.__used_songs] 
        self.__current_song=random.choice(not_used_songs)
        
    def start(self,search):
        self.__setPlaylistSongs(search)
        self.__setCurrentSong()
        options_songs=[None,None]
        random_index=random.randint(0,1)
        options_songs[random_index]=self.__current_song.nombre
        self.__used_songs.append(self.__current_song.nombre)
        options_songs[random_index-1] = random.choice([song for song in self.__playlist_songs if song.nombre not in self.__used_songs]).nombre
        self.__button1 = Button(25, 200, 350, 100, options_songs[0], Constants.CYAN, Constants.BLUE, self.__font)
        self.__button2 = Button(425, 200, 350, 100, options_songs[1], Constants.CYAN, Constants.BLUE, self.__font)
        self.__mixer = Mixer(self.__current_song.preview_url)
        self.__mixer.play()


    def changeButtons(self,value,screen):
        self.__used_songs.append(self.__current_song.nombre)
        self.__setCurrentSong()
        options_songs=[None,None]
        random_index=random.randint(0,1)
        options_songs[random_index]=self.__current_song.nombre
        self.__used_songs.append(self.__current_song.nombre)
        options_songs[random_index-1] = random.choice([song for song in self.__playlist_songs if song.nombre not in self.__used_songs]).nombre
        self.__button1 = Button(25, 200, 350, 100, options_songs[0], Constants.CYAN, Constants.BLUE, self.__font)
        self.__button2 = Button(425, 200, 350, 100, options_songs[1], Constants.CYAN, Constants.BLUE, self.__font)
        if value =="Correct":
            screen.fill(Constants.GREEN)
            pygame.display.flip()
            time.sleep(0.5)
        elif value =="Incorrect":
            screen.fill(Constants.RED)
            pygame.display.flip()
            time.sleep(0.5)
        else:
            raise ValueError("Unknow value for changeButtons. Value must be Correct or Incorrect")
        self.__mixer.changeSong(self.__current_song.preview_url)
    
    def drawscore(self,screen):
        text=f"Puntaje : {self.__player.score}"
        text_surf = self.__font.render(text, True, Constants.BLACK) #El True habilita antialiasing 
        text_rect = text_surf.get_rect(center=(Constants.SCREEN_WIDTH//8,Constants.SCREEN_HEIGHT//8)) # // es division entera
        screen.blit(text_surf, text_rect)

    def drawButtons(self,screen):
        self.__button1.draw(screen)
        self.__button2.draw(screen)

#creo que esta lista
class TextBox:
    def __init__(self, x, y, w, h, font):
        self.__rect = pygame.Rect(x, y, w, h)
        self.__color = Constants.LIGHT_GRAY
        self.__text = ''
        self.__font = font
        self.__txt_surface = self.__font.render(self.text, True, Constants.BLACK)
        self.__active = False
        self.__return_key_pressed = False

    #getters
    @property
    def return_key_pressed(self):
        return self.__return_key_pressed

    @property
    def text(self):
        return self.__text
    
    @property
    def rect(self):
        return self.__rect
    
    @property
    def color(self):
        return self.__color
    
    @property
    def font(self):
        return self.__font
    
    @property
    def txt_surface(self):
        return self.__txt_surface
    
    @property
    def active(self):
        return self.__active
    
    @text.setter
    def text(self, text_nuevo):
        if isinstance(text_nuevo, str):
            self.__text = text_nuevo
        else:
            raise ValueError("el texto debe ser un string")
        
    @color.setter
    def color(self, color_nuevo):
        self.__color = color_nuevo

    @rect.setter
    def rect(self, rect_nuevo):
        self.__rect = rect_nuevo

    @font.setter
    def font(self, font_nuevo):
        self.__font = font_nuevo

    @txt_surface.setter
    def txt_surface(self, txt_surface_nuevo):
        self.__txt_surface = txt_surface_nuevo

    @active.setter
    def active(self, active_nuevo):
        if isinstance(active_nuevo, bool):
            self.__active = active_nuevo
        else:
            raise ValueError("el active debe ser un tipo Bool")
        
    @return_key_pressed.setter
    def return_key_pressed(self, return_key_pressed_nuevo):
        if isinstance(return_key_pressed_nuevo, bool):
            self.__return_key_pressed = return_key_pressed_nuevo
        else:
            raise ValueError("el return_key_pressed debe ser un tipo Bool")

    #métodos

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__rect.collidepoint(event.pos):
                self.__active = not self.__active
            else:
                self.__active = False
            self.__color = Constants.BLACK if self.__active else Constants.LIGHT_GRAY #cambia el color de la caja de texto

        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_RETURN:
                    if len(self.__text) >= 3:
                        self.__return_key_pressed=True
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    if len(self.__text) < 20:
                        self.__text += event.unicode
                self.__txt_surface = self.__font.render(self.__text, True, Constants.BLACK) #carga el nuevo texto
        
    def update(self):
        width = max(200, self.__txt_surface.get_width()+10)
        self.__rect.w = width

    def draw(self, screen):
        # dibuja la caja del texto
        pygame.draw.rect(screen, self.__color, self.__rect, 2)
        # dibuja el texto
        screen.blit(self.__txt_surface, (self.__rect.x+5, self.__rect.y+5))

#creo que esta lista
class MenuScreen:
    def __init__(self):
        self.__text_box = TextBox(300, 250, 200, 32, pygame.font.Font(None, 25))
        self.__font = pygame.font.Font(None, 35)

    @property
    def text_box(self):
        return self.__text_box
    
    @property
    def font(self):
        return self.__font

    @text_box.setter
    def text_box(self, text_box_nuevo):
        self.__text_box = text_box_nuevo

    @font.setter
    def font(self, font_nuevo):
        self.__font = font_nuevo

    #métodos

    def drawText(self,screen):
        txt_surface = self.__font.render("Escribe el género de música con el que deseas jugar", True, Constants.BLACK)
        screen.blit(txt_surface, ((Constants.SCREEN_WIDTH//5)-60,Constants.SCREEN_HEIGHT//4))
    
    def drawLoadingScreen(self,screen):
        txt_surface = self.__font.render("Cargando...", True, Constants.BLACK)
        text_rect=txt_surface.get_rect(center=(Constants.SCREEN_WIDTH//2,Constants.SCREEN_HEIGHT//2))
        screen.blit(txt_surface, text_rect)

#creo que esta lista
class GameState:
    def __init__(self):
        self.__menu_state=True
        self.__game_screen_state=False

    
    @property
    def menu_state(self):
        return self.__menu_state

    @menu_state.setter
    def menu_state(self,value):
        if not isinstance (value,bool):
            raise ValueError("Menu state must be boolean")
        self.__menu_state=value

    @property
    def game_screen_state(self):
        return self.__game_screen_state    
    
    @game_screen_state.setter
    def game_screen_state(self,value):
        if not isinstance (value,bool):
            raise ValueError("GameScreen state must be boolean")
        self.__game_screen_state=value

class Mixer:

    def __init__(self,url):
        self.__url=url
  
    
    def __loadSong(self,url):
        response = requests.get(url)
        audio_stream = BytesIO(response.content)
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()

    def play(self):
        pygame.mixer.init()
        self.__loadSong(self.__url)
        


    def changeSong(self,url):
        self.__url=url
        self.__loadSong(url)

