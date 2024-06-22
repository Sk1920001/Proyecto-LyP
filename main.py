import pygame.display
from functions import obtener_token,buscar_playlist,playlist
import pygame
import requests
from io import BytesIO
import sys
import random
import time


class Constants:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0,255,255)
    LIGHT_GRAY = (200, 200, 200)
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=600



class Songs:
    def __init__(self,name,artist,preview_url):
        self.__name=name
        self.__artist=artist
        self.__preview_url=preview_url
    
    @property
    def name(self):
        return self.__name
    @property
    def url(self):   
        return self.__preview_url
    @property
    def artist(self):
        return self.__artist
    

class Player:
    def __init__(self,name):
        self.__name=name
        self.__score=0

  
    def changescore(self,value):
        if not isinstance(value,int):
            raise ValueError("Value must be an integer")
        self.__score+=value

    @property
    def score(self):
        return self.__score

    @property
    def name(self):
        return self.__name
    
        

    
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color,font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.font=font

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


class GameScreen:
    def __init__(self,player):
        self.__button1=None
        self.__button2=None
        self.__playlist_songs=[]
        self.__used_songs=[]
        self.__current_song=None
        self.__mixer=None
        self.__player=player
        self.__font=pygame.font.Font(None, 25)

    def __setPlaylistSongs(self,search):
        tok = obtener_token()
        id_playlist = buscar_playlist(tok, search)["id"]
        playlist_dict = playlist(tok,id_playlist)    
        cantidad_canciones = playlist_dict["tracks"]["total"]
        for i in range(0,cantidad_canciones,1):
            if(playlist_dict["tracks"]["items"][i]["track"]["preview_url"]==None):
                continue

            self.__playlist_songs.append(Songs(playlist_dict["tracks"]["items"][i]["track"]["name"],
                            playlist_dict["tracks"]["items"][i]["track"]["artists"][0]["name"],
                            playlist_dict["tracks"]["items"][i]["track"]["preview_url"]

            ))
        

    def __setCurrentSong(self):
        if len(self.__playlist_songs)==0:
            raise ValueError("Playlist cannot be empty")
        not_used_songs=[song for song in self.__playlist_songs if song.name not in self.__used_songs]
        self.__current_song=random.choice(not_used_songs)
        
    def start(self,search):
        self.__setPlaylistSongs(search)
        self.__setCurrentSong()
        options_songs=[None,None]
        random_index=random.randint(0,1)
        options_songs[random_index]=self.__current_song.name
        self.__used_songs.append(self.__current_song.name)
        options_songs[random_index-1]=random.choice([song for song in self.__playlist_songs if song.name not in self.__used_songs]).name
        self.__button1=Button(25, 200, 350, 100, options_songs[0], Constants.CYAN, Constants.BLUE,self.__font)
        self.__button2=Button(425, 200, 350, 100, options_songs[1], Constants.CYAN, Constants.BLUE,self.__font)
        self.__mixer=Mixer(self.__current_song.url)
        self.__mixer.play()


    def changeButtons(self,value,screen):
        self.__used_songs.append(self.__current_song.name)
        self.__setCurrentSong()
        options_songs=[None,None]
        random_index=random.randint(0,1)
        options_songs[random_index]=self.__current_song.name
        self.__used_songs.append(self.__current_song.name)
        options_songs[random_index-1]=random.choice([song for song in self.__playlist_songs if song.name not in self.__used_songs]).name
        self.__button1=Button(25, 200, 350, 100, options_songs[0], Constants.CYAN, Constants.BLUE,self.__font)
        self.__button2=Button(425, 200, 350, 100, options_songs[1], Constants.CYAN, Constants.BLUE,self.__font)
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
        self.__mixer.changeSong(self.__current_song.url)
    
    def drawscore(self,screen):
        text=f"Puntaje : {self.__player.score}"
        text_surf = self.__font.render(text, True, Constants.BLACK) #El True habilita antialiasing xddd
        text_rect = text_surf.get_rect(center=(Constants.SCREEN_WIDTH//8,Constants.SCREEN_HEIGHT//8)) # // es division entera
        screen.blit(text_surf, text_rect)

    def drawButtons(self,screen):
        self.__button1.draw(screen)
        self.__button2.draw(screen)

    @property
    def button1(self):
        return self.__button1
    @property
    def button2(self):
        return self.__button2
    @property
    def currentSong(self):
        return self.__current_song
    
class TextBox:
    def __init__(self, x, y, w, h, font):
        self.__rect = pygame.Rect(x, y, w, h)
        self.__color = Constants.LIGHT_GRAY
        self.__text = ''
        self.__font = font
        self.__txt_surface = self.__font.render(self.text, True, Constants.BLACK)
        self.__active = False
        self.__return_key_pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle the active state if the text box is clicked
            if self.__rect.collidepoint(event.pos):
                self.__active = not self.__active
            else:
                self.__active = False
            # Change the text box color
            self.__color = Constants.BLACK if self.__active else Constants.LIGHT_GRAY

        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_RETURN:
                    if len(self.__text)>=3:
                        self.__return_key_pressed=True
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    if len(self.__text)<20:
                        self.__text += event.unicode
                # Render the new text
                self.__txt_surface = self.__font.render(self.__text, True, Constants.BLACK)
        
    @property
    def return_key_pressed(self):
        return self.__return_key_pressed

    def update(self):
        # Adjust the width of the text box as the text changes
        width = max(200, self.__txt_surface.get_width()+10)
        self.__rect.w = width

    def draw(self, screen):
        # Draw the text box
        pygame.draw.rect(screen, self.__color, self.__rect, 2)
        # Draw the text
        screen.blit(self.__txt_surface, (self.__rect.x+5, self.__rect.y+5))

    @property
    def text(self):
        return self.__text


class MenuScreen:
    def __init__(self):
        self.__text_box=TextBox(300, 250, 200, 32, pygame.font.Font(None, 25))
        self.__filter=None
        self.__font=pygame.font.Font(None, 35)

    @property
    def text_box(self):
        return self.__text_box

    @property                                #definir property antes de su respectivo setter
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, text):
        self.__filter = text

    def drawText(self,screen):
        txt_surface = self.__font.render("Escribe el género de música con el que deseas jugar", True, Constants.BLACK)
        screen.blit(txt_surface, ((Constants.SCREEN_WIDTH//5)-60,Constants.SCREEN_HEIGHT//4))
    
    def drawLoadingScreen(self,screen):
        txt_surface = self.__font.render("Cargando...", True, Constants.BLACK)
        text_rect=txt_surface.get_rect(center=(Constants.SCREEN_WIDTH//2,Constants.SCREEN_HEIGHT//2))
        screen.blit(txt_surface, text_rect)


    


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




def main():
    screen=pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
    pygame.font.init()
    pygame.display.set_caption("Juegito")    
    game_state=GameState()
    menu_screen=MenuScreen()
    running=True


    while running:
        
        if game_state.menu_state==True and game_state.game_screen_state==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif menu_screen.text_box.return_key_pressed==True:
                    game_state.menu_state=False
                    game_state.game_screen_state=True
                    screen.fill(Constants.WHITE)
                    menu_screen.drawLoadingScreen(screen)
                    pygame.display.flip() 
                    player=Player("Benja")
                    game=GameScreen(player)
                    game.start(menu_screen.text_box.text)
                    buttons = [game.button1, game.button2]
                    clock=pygame.time.Clock()
                    elapsed_time=0
                    break
                menu_screen.text_box.handle_event(event)
                
            if game_state.menu_state==True and game_state.game_screen_state==False:
                menu_screen.text_box.update()
                screen.fill(Constants.WHITE)
                menu_screen.text_box.draw(screen)
                menu_screen.drawText(screen)
                pygame.display.flip()
        
        elif game_state.menu_state==False and game_state.game_screen_state==True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.click(game.currentSong.name) ==True:
                                    player.changescore(1)
                                    game.changeButtons("Correct",screen)
                                    buttons = [game.button1, game.button2]
                                    elapsed_time=0
                                    continue
                                else:
                                    game.changeButtons("Incorrect",screen)
                                    buttons = [game.button1, game.button2]
                                    elapsed_time=0
                                    continue

            # Actualizar estado de los botones
            for button in buttons:
                button.update()
                
            
            elapsed_time += clock.tick(60) / 1000  # Convierte los milisegundos a segundos (limita a 60 frames por segundo y calcula el paso de un frame)
            if elapsed_time >= 10:
                game.changeButtons("Incorrect",screen)
                buttons = [game.button1, game.button2]
                elapsed_time = 0

            # Dibujar en la pantalla
            screen.fill(Constants.WHITE)
            game.drawButtons(screen)
            game.drawscore(screen)
            pygame.display.flip() #no lo pongo dentro de la clase ya que parpadearian los objetos, ya que estaría haciendo flip dos veces
    
    pygame.quit()
    sys.exit()


if __name__== "__main__":
    main()