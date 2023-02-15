import sys
import pygame
from pygame.locals import QUIT
import time
import random
#Seteamos alto y ancho en variables
ANCHO = 1300
ALTO = 800
pygame.mixer.init()
bot = False

#Definimos sonidos
sound_hit_ball = pygame.mixer.Sound("PongBase/Assets/sound_assets/hit.mp3")
sound_hit_wall = pygame.mixer.Sound("PongBase/Assets/sound_assets/hit_wall.mp3")
sound_win_round = pygame.mixer.Sound("PongBase/Assets/sound_assets/win_round.mp3")
sound_lose_round = pygame.mixer.Sound("PongBase/Assets/sound_assets/lose_round.mp3")
sound_ready_fight = pygame.mixer.Sound("PongBase/Assets/sound_assets/ready-fight.mp3")
sound_lose_game = pygame.mixer.Sound("PongBase/Assets/sound_assets/game_over.mp3")
sound_win_game = pygame.mixer.Sound("PongBase/Assets/sound_assets/game_winned.mp3")
background_sound = pygame.mixer.Sound("PongBase/Assets/sound_assets/background_sound.mp3")
sound_pause = pygame.mixer.Sound("PongBase/Assets/sound_assets/sound_pause.mp3")
sound_resume = pygame.mixer.Sound("PongBase/Assets/sound_assets/sound_resume.mp3")
sound_menu = pygame.mixer.Sound("PongBase/Assets/sound_assets/menu_song.mp3")
sound_picker_menu = pygame.mixer.Sound("PongBase/Assets/sound_assets/button.mp3")

LIMITE_PUNTOS = 7

POSICIONTEXT_X = 50
POSICIONTEXT_Y = 750

VELOCIDAD_RAQUETAIA = 4.5

#Seteamos FPS en variable
FPS = 100

#Seteamos Background color en variable
COLOR = (0,0,0)
BLANCO = (255,255,255)

#Definimos la clase pelota
class Pelota:
    #Definimos el constructor
    def __init__(self,imagen_fichero):
        #Cargamos el fichero
        self.imagen = pygame.image.load(imagen_fichero).convert_alpha()
        #Indicamos el tamaño de la pelota con el tamaño de la imagenes por pixeles
        self.ancho, self.alto = self.imagen.get_size()
        
        #Para setear la coordenada/posicion inicial al centro del ancho
        self.x = ANCHO/2 - self.ancho/2
        #Para setear la coordenada/posicion inicial al centro del alto
        self.y = ALTO/2 - self.alto/2
        #Cooredenadas de posicion con vector, es lo mismo que el seteo de x e y
        #self.posicion = (ANCHO/2 - self.ancho/2,ALTO/2 - self.alto/2)
        
        #Seteamos la direcion de movimiento incial x
        self.dir_x = random.choice([-5,5])
        #Seteamos la direcion de movimiento incial y
        self.dir_y = random.choice([-5,5])
    
    #Creamos un metodo para mover la pelota        
    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y


    #Creamos un metodo para rebotar/colisionar con los limites
    def colision_limite(self):
        if self.x <= 0:
            self.dir_x = -self.dir_x


        if self.x + self.ancho >= ANCHO:
            self.dir_x = -self.dir_x   
                     
        if self.y <= 0:
            self.dir_y = -self.dir_y
            sound_hit_wall.play()
        
        if self.y + self.alto >= ALTO:
            self.dir_y = -self.dir_y
            sound_hit_wall.play()

class Raqueta:
    def __init__(self):
        self.image = pygame.image.load("PongBase/Assets/raqueta_blanca.png").convert_alpha()
        self.ancho , self.alto = self.image.get_size()
        self.score = 0
        self.x = 0
        self.y = ALTO/2 - self.alto/2
        self.dir_y = 0

    def mover(self):
         self.y += self.dir_y
         if self.y <= 0:
             self.y = 0
         if self.y + self.alto >= ALTO:
             self.y = ALTO - self.alto
             
    def golpear(self,pelota):
        if (pelota.x < self.x + self.ancho and pelota.x > self.x and pelota.y + pelota.alto > self.y and pelota.y < self.y + self.alto):
            sound_hit_ball.play()            
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
                
    def mover_ia(self,pelota):
        if self.y > pelota.y:
            self.dir_y = -VELOCIDAD_RAQUETAIA
        
        elif self.y < pelota.y:
            self.dir_y = VELOCIDAD_RAQUETAIA
        else:
            self.dir_y = 0
        
        self.y += self.dir_y
        if self.y + self.alto >= ALTO:
             self.y = ALTO - self.alto
        
    def golpear_ia(self,pelota):
        if (pelota.x + pelota.ancho > self.x and pelota.x < self.x + self.ancho and pelota.y + pelota.alto > self.y and pelota.y < self.y + self.alto):
            sound_hit_ball.play()
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - self.ancho


class Menu:
    
    def guarda_conf(self,vol,mute):
        with open("PongBase/Assets/Config/config.cfg","w") as f:
            f.write(str(vol)+'\n')
            f.write(str(mute))
    
    def get_vol(self):
        file = open("PongBase/Assets/Config/config.cfg","r")
        contenido = file.readlines()
        return int(contenido[0])
    
    def get_mute(self):
        file = open("PongBase/Assets/Config/config.cfg","r")
        contenido = file.readlines()
        if(contenido[1]=="True"):
            return True
        else:
            return False

    def inicia_menu(self):
        sound_menu.play()
        MUTE = self.get_mute()
        VOLUMEN = self.get_vol()
        self.muteornot(MUTE,VOLUMEN)
        #Seteamos display con el ancho y alto
        ventana = pygame.display.set_mode((ANCHO,ALTO))
        #Seteamos titulo
        pygame.display.set_caption("PONG")
        seleccion_menu = 0
        elementos_menu = 4
        element1 ="PLAYER VS IA"
        element2 = "JUGADOR 1 VS JUGADOR 2"
        element3 = "OPCIONES"
        element4 = "SALIR"
        menu = True
        opciones = False
        seleccion_activa = False
        menu_font = pygame.font.SysFont('Impact', 100, False, False)
        menu_font1 = pygame.font.SysFont('Impact', 100, False, True)
        opciones_font = pygame.font.SysFont('Impact', 80, False, False)
        opciones_font1 = pygame.font.SysFont('Impact', 80, False, True)
        while menu:
            seleccion_opciones = 0
            while opciones:
                pygame.display.flip()
                elementos_opciones = 3
                opcion1 ="VOLUMEN"
                subopcion1 = str(VOLUMEN) + "%"
                opcion2 = "MUTE"
                
                if MUTE:
                    subopcion2 = "YES"
                else:
                    subopcion2 = "NO"
                opcion3 = "SALIR"
                seleccion_activa_opciones = False
                if seleccion_opciones == 0:
                    itemp_1 = opciones_font1.render(opcion1, True, (255,255,255))
                    subitemp_1 = opciones_font.render(subopcion1, True, (255,255,255))
                    itemp_2 = opciones_font.render(opcion2, True, (255,255,255))
                    subitemp_2 = opciones_font.render(subopcion2, True, (255,255,255))
                    itemp_3 = opciones_font.render(opcion3, True, (255,255,255))
                elif seleccion_opciones == 1:
                    itemp_1 = opciones_font.render(opcion1, True, (255,255,255))
                    subitemp_1 = opciones_font.render(subopcion1, True, (255,255,255))
                    itemp_2 = opciones_font1.render(opcion2, True, (255,255,255))
                    subitemp_2 = opciones_font.render(subopcion2, True, (255,255,255))
                    itemp_3 = opciones_font.render(opcion3, True, (255,255,255))
                elif seleccion_opciones == 2:
                    itemp_1 = opciones_font.render(opcion1, True, (255,255,255))
                    subitemp_1 = opciones_font.render(subopcion1, True, (255,255,255))
                    itemp_2 = opciones_font.render(opcion2, True, (255,255,255))
                    subitemp_2 = opciones_font.render(subopcion2, True, (255,255,255))
                    itemp_3 = opciones_font1.render(opcion3, True, (255,255,255))
                else:
                    itemp_1 = opciones_font.render(opcion1, True, (255,255,255))
                    itemp_2 = opciones_font.render(opcion2, True, (255,255,255))
                    itemp_3 = opciones_font.render(opcion3, True, (255,255,255))
                
                ventana.blit(itemp_1,(250,200))
                ventana.blit(itemp_2,(250,300))
                ventana.blit(itemp_3, (250,400))
                ventana.blit(subitemp_1, (800,200))
                ventana.blit(subitemp_2, (800,300))
        
                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if seleccion_opciones >= 0 and seleccion_opciones < elementos_opciones:
                            if seleccion_opciones == 0 and VOLUMEN <= 95:
                                if evento.key == pygame.K_RIGHT:
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    VOLUMEN += 5
                                    if MUTE == False:
                                        self.set_volume(VOLUMEN)
                                    sound_picker_menu.play()
                            if seleccion_opciones == 0 and VOLUMEN >= 5:
                                if evento.key == pygame.K_LEFT:
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    VOLUMEN -= 5
                                    if MUTE == False:
                                        self.set_volume(VOLUMEN)
                                    sound_picker_menu.play()
                            if seleccion_opciones == 1:
                                if evento.key == pygame.K_RIGHT:
                                    MUTE = not MUTE
                                    self.muteornot(MUTE, VOLUMEN)
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    sound_picker_menu.play()
                                elif evento.key == pygame.K_LEFT:  
                                    MUTE = not MUTE
                                    self.muteornot(MUTE, VOLUMEN)
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    sound_picker_menu.play()
                            
                            if evento.key == pygame.K_UP:
                                if seleccion_opciones >= 1:
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    seleccion_opciones -= 1
                                    sound_picker_menu.play()
                            elif evento.key == pygame.K_DOWN:
                                if seleccion_opciones < elementos_opciones - 1:
                                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                                    sound_picker_menu.play()
                                    seleccion_opciones += 1
                        if evento.key == pygame.K_SPACE:
                            seleccion_activa_opciones = True

                if seleccion_opciones == 0 and seleccion_activa_opciones:
                    
                    seleccion_activa_opciones = False
                elif seleccion_opciones == 1 and seleccion_activa_opciones:

                    seleccion_activa_opciones = False
                elif seleccion_opciones == 2 and seleccion_activa_opciones:
                    opciones = False
                    self.guarda_conf(VOLUMEN,MUTE)
                    ventana = pygame.display.set_mode((ANCHO,ALTO))
                    seleccion_activa_opciones = False
                
            if seleccion_menu == 0:
                item_1 = menu_font1.render(element1, True, (255,255,255))
                item_2 = menu_font.render(element2, True, (255,255,255))
                item_3 = menu_font.render(element3, True, (255,255,255))
                item_4 = menu_font.render(element4, True, (255,255,255))
            elif seleccion_menu == 1:
                item_1 = menu_font.render(element1, True, (255,255,255))
                item_2 = menu_font1.render(element2, True, (255,255,255))
                item_3 = menu_font.render(element3, True, (255,255,255))
                item_4 = menu_font.render(element4, True, (255,255,255))
            elif seleccion_menu == 2:
                item_1 = menu_font.render(element1, True, (255,255,255))
                item_2 = menu_font.render(element2, True, (255,255,255))
                item_3 = menu_font1.render(element3, True, (255,255,255))
                item_4 = menu_font.render(element4, True, (255,255,255))
            elif seleccion_menu == 3:
                item_1 = menu_font.render(element1, True, (255,255,255))
                item_2 = menu_font.render(element2, True, (255,255,255))
                item_3 = menu_font.render(element3, True, (255,255,255))
                item_4 = menu_font1.render(element4, True, (255,255,255))
            else:
                item_1 = menu_font.render(element1, True, (255,255,255))
                item_2 = menu_font.render(element2, True, (255,255,255))
                item_3 = menu_font.render(element3, True, (255,255,255))
                item_4 = menu_font.render(element4, True, (255,255,255))

            ventana.blit(item_1,(100,200))
            ventana.blit(item_2,(200,300))
            ventana.blit(item_3,(300,400))
            ventana.blit(item_4,(400,500))

            for evento in pygame.event.get():
                if evento.type == QUIT:
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if seleccion_menu >= 0 and seleccion_menu < elementos_menu:
                        if evento.key == pygame.K_UP:
                            if seleccion_menu >= 1:
                                ventana = pygame.display.set_mode((ANCHO,ALTO))
                                seleccion_menu -= 1
                                sound_picker_menu.play()
                        elif evento.key == pygame.K_DOWN:
                            if seleccion_menu < elementos_menu - 1:
                                ventana = pygame.display.set_mode((ANCHO,ALTO))
                                sound_picker_menu.play()
                                seleccion_menu += 1
                    if evento.key == pygame.K_SPACE:
                        seleccion_activa = True
                            
            if seleccion_menu == 0 and seleccion_activa:
                menu = False
                bot = True
                partida = Juego()
                ventana = pygame.display.set_mode((ANCHO,ALTO))
                partida.inicia_juego(ventana, bot)
                seleccion_activa = False
            elif seleccion_menu == 1 and seleccion_activa:
                menu = False
                bot = False
                partida = Juego()
                ventana = pygame.display.set_mode((ANCHO,ALTO))
                partida.inicia_juego(ventana,bot)
                seleccion_activa = False
            elif seleccion_menu == 2 and seleccion_activa:
                opciones = True
                ventana = pygame.display.set_mode((ANCHO,ALTO))
                seleccion_activa = False
            elif seleccion_menu == 3 and seleccion_activa:
                menu = False 
                seleccion_activa = False
                sys.exit()
              
            pygame.display.flip()
        
        time.sleep(10)
    
    def set_volume(self,vol):
        sound_hit_ball.set_volume(vol/100)
        sound_hit_wall.set_volume(vol/1000)
        sound_win_round.set_volume(vol/100)
        sound_lose_round.set_volume(vol/100)
        sound_ready_fight.set_volume(vol/100)
        sound_lose_game.set_volume(vol/100)
        sound_win_game.set_volume(vol/100)
        background_sound.set_volume(vol/100)
        sound_pause.set_volume(vol/100)
        sound_resume.set_volume(vol/100)
        sound_menu.set_volume(vol/100)
        sound_picker_menu.set_volume(vol/100)
     
    def set_volumeTo0(self):
        sound_hit_ball.set_volume(0)
        sound_hit_wall.set_volume(0)
        sound_win_round.set_volume(0)
        sound_lose_round.set_volume(0)
        sound_ready_fight.set_volume(0)
        sound_lose_game.set_volume(0)
        sound_win_game.set_volume(0)
        background_sound.set_volume(0)
        sound_pause.set_volume(0)
        sound_resume.set_volume(0)
        sound_menu.set_volume(0)
        sound_picker_menu.set_volume(0)
    
        
    def muteornot(self,MUTE,VOLUMEN):
        if MUTE == True:
            self.set_volume(0)
        elif MUTE == False:
            self.set_volume(VOLUMEN)    
            
              
class Juego:
    def inicia_juego(self,ventana,bot):
        pygame.init()
        sound_menu.stop()
        pelota = Pelota("PongBase/Assets/bola_blanca.png")
        raquetaJugador = Raqueta()
        raquetaJugador.x = 20
        raquetaIA = Raqueta()
        raquetaIA.x = ANCHO - raquetaIA.ancho -20
        font = pygame.font.SysFont('Impact', 70)
        fontText = pygame.font.SysFont('Impact', 40)
        jugando = False
        sound_ready_fight.play()
        time.sleep(3)
        background_sound.play()
        saque = False
        #findepartida = False
        paused = False
        jugando = True
        #Seteamos bucle juego
        while jugando:
            while saque:
                for evento in pygame.event.get():
                    if evento.type == QUIT:
                        jugando = False
                        saque = False
                        sys.exit()
                    if evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_SPACE:
                            pelota.dir_x = random.choice([-5,5])
                            pelota.dir_y = random.choice([-5,5])
                            saque = False
            
            pelota.mover()
            pelota.colision_limite()
            raquetaJugador.mover()
            raquetaJugador.golpear(pelota)            
            if bot:
                raquetaIA.mover_ia(pelota)
                raquetaIA.golpear_ia(pelota) 
            else:
                raquetaIA.mover()
                raquetaIA.golpear_ia(pelota)

            mensajeEsperaLanzamiento = ""
            scorePlayer = font.render(str(raquetaJugador.score), True, (255,255,255))
            scoreIA = font.render(str(raquetaIA.score), True, (255,255,255))
            waitText = fontText.render(mensajeEsperaLanzamiento,True,(255,255,255))
            #Se añade score a la IA si pasa el limite derecho
            if scoreIA or scorePlayer < LIMITE_PUNTOS:
                if pelota.x <= 0:
                    sound_lose_round.play()
                    raquetaIA.score += 1
                    raquetaJugador.dir_y = 0
                    raquetaIA.dir_y = 0 
                    pelota.x = raquetaJugador.x + raquetaJugador.ancho
                    pelota.y = ALTO/2 - pelota.alto/2
                    pelota.dir_x = 0
                    pelota.dir_y = 0
                    raquetaIA.y = ALTO/2 - raquetaIA.alto/2
                    raquetaJugador.y = ALTO/2 - raquetaJugador.alto/2
                    mensajeEsperaLanzamiento = "PULSA ESPACIO PARA SACAR"
                    waitText = fontText.render(mensajeEsperaLanzamiento,True,(255,255,255))
                    scoreIA = font.render(str(raquetaIA.score), True, (255,255,255))
                    ventana.blit(waitText,(POSICIONTEXT_X,POSICIONTEXT_Y))
                    ventana.blit(scoreIA,(ANCHO-200,50))
                    saque = True
                #Se añade score al jugador en el momento que la pelota colisione con el limite izquierdo
                if pelota.x + pelota.ancho >= ANCHO:
                    sound_win_round.play()
                    raquetaJugador.score +=1
                    raquetaJugador.dir_y = 0
                    raquetaIA.dir_y = 0 
                    pelota.x = raquetaIA.x - raquetaIA.ancho
                    pelota.y = ALTO/2 - pelota.alto/2
                    pelota.dir_x = -pelota.dir_x
                    pelota.dir_y = -pelota.dir_y
                    raquetaIA.y = ALTO/2 - raquetaIA.alto/2
                    raquetaJugador.y = ALTO/2 - raquetaJugador.alto/2
                    mensajeEsperaLanzamiento = "PULSA ESPACIO PARA SACAR"
                    waitText = fontText.render(mensajeEsperaLanzamiento,True,(255,255,255))
                    scorePlayer = font.render(str(raquetaJugador.score), True, (255,255,255))
                    ventana.blit(scorePlayer,(200,50))
                    ventana.blit(waitText,(POSICIONTEXT_X,POSICIONTEXT_Y))
                    saque = True
                          
            #Establecemos el color de relleno de la ventana
            ventana.fill(COLOR)

            pygame.draw.line(ventana,(BLANCO),(ANCHO/2,ALTO),(ANCHO/2,0))

            #Repintar pelota
            ventana.blit(pelota.imagen,(pelota.x,pelota.y))
            ventana.blit(raquetaJugador.image,(raquetaJugador.x,raquetaJugador.y))
            ventana.blit(raquetaIA.image,(raquetaIA.x,raquetaIA.y))
            ventana.blit(scorePlayer,(200,50))
            ventana.blit(scoreIA,(ANCHO-200,50))
            ventana.blit(waitText,(POSICIONTEXT_X,POSICIONTEXT_Y))

            #Recorremos los eventos y comprobamos el de salida para cerrar correctamente sin fallos
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    jugando = False
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_w:
                        raquetaJugador.dir_y = -5
                    if evento.key == pygame.K_s:
                        raquetaJugador.dir_y = 5
                    if bot == False:   
                        if evento.key == pygame.K_UP:
                            raquetaIA.dir_y = -5      
                        if evento.key == pygame.K_DOWN:
                            raquetaIA.dir_y = 5
                    if evento.key == pygame.K_ESCAPE:
                        sound_pause.play()
                        background_sound.set_volume(0)
                        paused = not paused                        
                if evento.type == pygame.KEYUP:     
                    if evento.key == pygame.K_w:
                        if raquetaJugador.dir_y == -5:
                            raquetaJugador.dir_y = 0
                    if evento.key == pygame.K_s:
                        if raquetaJugador.dir_y == 5:
                            raquetaJugador.dir_y = 0
                    if bot == False:        
                        if evento.key == pygame.K_UP:
                            if raquetaIA.dir_y == -5:
                                raquetaIA.dir_y = 0
                        if evento.key == pygame.K_DOWN:
                            if raquetaIA.dir_y == 5:
                                raquetaIA.dir_y = 0
                                       
            while paused:
                raquetaIA.dir_y = 0
                raquetaJugador.dir_y = 0
                text_paused = fontText.render("PAUSED", True, (255,255,255))
                ventana.blit(text_paused,((ANCHO-80)/2,ALTO/2))
                pygame.display.flip()
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        jugando = False
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            sound_resume.play()
                            paused = False       
            
            if raquetaIA.score >= LIMITE_PUNTOS or raquetaJugador.score >= LIMITE_PUNTOS:
                text_paused = font.render("FIN DE LA PARTIDA", True, (255,255,255))
                ventana.blit(text_paused,(300,ALTO/4))
                if raquetaJugador.score >= LIMITE_PUNTOS:
                    sound_win_game.play()
                    text_win = font.render("HA GANADO PLAYER 1!", True,(255,255,255))
                    ventana.blit(text_win,(300,ALTO/2))
                    jugando = False
                elif raquetaIA.score >= LIMITE_PUNTOS and bot == True:
                    sound_lose_game.play()
                    text_win = font.render("HAS PERDIDO! LA IA HA GANADO!", True, (255,255,255))
                    ventana.blit(text_win,(300,ALTO/2))    
                    jugando = False
                elif raquetaIA.score >= LIMITE_PUNTOS and bot == False:
                    sound_lose_game.play()
                    text_win = font.render("HA GANADO PLAYER 2!", True, (255,255,255))
                    ventana.blit(text_win,(300,ALTO/2))    
                    jugando = False
                        
            #Para acutalizar el display
            pygame.display.update()
            #Establemeos tiempo de metronomo/trabajo con los FPS declarados antes.
            pygame.time.Clock().tick(FPS)
            
#Definimos clase main
def main():
    pygame.init()
    menu = Menu()
    menu.inicia_menu()

    
    
if __name__ == "__main__":
    main()