from Funciones import *
from Clases import *
import sys


def main():
    screen=pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT))
    pygame.font.init()
    pygame.display.set_caption("Juegito")    
    game_state = GameState()
    menu_screen = MenuScreen()
    
    running = True

    while running:
        if (game_state.menu_state == True) and (game_state.game_screen_state == False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif menu_screen.text_box.return_key_pressed == True:
                    game_state.menu_state = False
                    game_state.game_screen_state = True
                    screen.fill(Constants.WHITE)
                    menu_screen.drawLoadingScreen(screen)
                    pygame.display.flip() 
                    player = Player("El master del juego")
                    game = GameScreen(player)
                    game.start(menu_screen.text_box.text)
                    buttons = [game.button1, game.button2]
                    clock=pygame.time.Clock()
                    elapsed_time = 0
                    break
                menu_screen.text_box.handle_event(event)
                
            if (game_state.menu_state == True) and (game_state.game_screen_state == False):
                menu_screen.text_box.update()
                screen.fill(Constants.WHITE)
                menu_screen.text_box.draw(screen)
                menu_screen.drawText(screen)
                pygame.display.flip()
        
        elif (game_state.menu_state == False) and (game_state.game_screen_state == True):
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
    sys.exit()


if __name__== "__main__":
    main()
