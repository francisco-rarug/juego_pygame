import pygame
from pygame.locals import *
import sys
from constantes import *
import json


music_playing = True


        

def nivel_1():

    from player import Player
    from enemigo import Enemy
    from plataforma import Plataform
    from trampas import Trampa
    from poderes import Poderes
    from enemigo2 import Enemy_2
    from nivel_2 import nivel_2
    from main import main

    def toggle_music():
        global music_playing

        if music_playing:
            pygame.mixer.music.pause()
            music_playing = False
            player_1.musica=False
            enemigos.musica=False
            
        else:
            pygame.mixer.music.unpause()
            music_playing = True
            player_1.musica=True
            enemigos.musica=True

    flags = DOUBLEBUF

    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags, 16)
    pygame.init()
    clock = pygame.time.Clock()

    imagen_fondo = pygame.image.load("images/locations/set_bg_01/forest/robot_background.jpg").convert()
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    #Grupo de sprites
    estrella = pygame.sprite.Group()
    poder = pygame.sprite.Group()
    trampa=pygame.sprite.Group()
    enemigos=pygame.sprite.Group()
    enemigo2=pygame.sprite.Group()
    vidas_extras=pygame.sprite.Group()

    pygame.init()
    pygame.mixer.init()

    #Variables varias
    score_timer = 0
    time_limit = 60
    elapsed_time = 0
    
    with open("nivel_1.json", "r") as archivo:
        contenido_json = json.load(archivo)

    # Obtener las plataformas del nivel 1
    plataformas_nivel_1 = contenido_json["plataformas"]

    # Crear una lista de plataformas
    plataformas = []

    # Recorrer las plataformas del nivel 1
    for plataforma in plataformas_nivel_1:
        x = plataforma["x"]
        y = plataforma["y"]
        width = plataforma["width"]
        height = plataforma["height"]
        type = plataforma["type"]
        
        # Crear la plataforma y agregarla a la lista
        nueva_plataforma = Plataform(x, y, width, height, type)
        plataformas.append(nueva_plataforma)

    #Inicializar el personaje 1 con sus atributos correspondientes
    player_1 = Player(x=0, y=500, speed_walk=12, speed_run=24, gravity=10, jump_power=50, frame_rate_ms=100, move_rate_ms=50, jump_height=110, p_scale=0.2, interval_time_jump=300, estrella=estrella, poderes=poder, vidas_extra=vidas_extras, trampas=trampa, enemigos=enemigos, enemigo_2=enemigo2, numero_player=1, musica=True)

    #Inicializar los enemigos con sus atributos correspondientes
    enemy_list=[]
    enemy_list.append(Enemy(x=300, y=330, speed_walk=6, speed_run=8, gravity=4, frame_rate_ms=50, move_rate_ms=50, jump_power=30, jump_height=140, p_scale=0.08,  numero_enemy=1, musica=True))
    enemy_list.append(Enemy(x=950, y=330, speed_walk=6, speed_run=8, gravity=4, frame_rate_ms=50, move_rate_ms=50, jump_power=30, jump_height=140, p_scale=0.08,  numero_enemy=1, musica=True))
    enemigos.add(enemy_list)

    enemy_list_2=[]
    enemy_list_2.append(Enemy_2(x=900, y=175, p_scale=1, numero_enemy_2=1))
    enemigo2.add(enemy_list_2)

    #Declaracion y aplicacion de las trampas
    trampas_list=[]
    trampas_list.append(Trampa(500, 380, "images/Object/trampas/Spike.png", 0.2))
    trampa.add(trampas_list)

    #Declaracion y aplicacion de las estrellas
    star_list = [(115, 360), (300, 170), (1115, 60)]  
    for posicion in star_list:
        x = posicion[0]
        y = posicion[1]
        star= Poderes(x, y, "images/Object/coin/star.png", scale=0.3)
        estrella.add(star)

    #Declaracion y aplicacion de los poderes
    poderes = [(250, 170)]  
    for posicion in poderes:
        x = posicion[0]
        y = posicion[1]
        poderes = Poderes(x, y, "images/Object/coin/papas.png", scale=2)
        poder.add(poderes)

    pygame.mixer.music.load("audio/vgm-atmospheric-deepspace.mp3")
    volumen = 0.4
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loops=-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                pygame.mixer.music.play(loops=-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if marco_1_rect is not None and marco_2_rect is not None and marco_3_rect is not None:
                    if marco_1_rect.collidepoint(event.pos):
                        player_1.pause=False
                    elif marco_2_rect.collidepoint(event.pos):
                        nivel_1()
                    elif marco_3_rect.collidepoint(event.pos):
                        main()

                if marco_1_rect_win is not None and marco_2_rect_win is not None and marco_3_rect_win is not None:
                    if marco_1_rect_win.collidepoint(event.pos):
                        nivel_1()
                    elif marco_2_rect_win.collidepoint(event.pos):
                        main()
                    elif marco_3_rect_win.collidepoint(event.pos):
                        nivel_2()
                
                if marco_1_rect_lose is not None and marco_2_rect_lose is not None:
                    if marco_1_rect_lose.collidepoint(event.pos):
                        main()
                    elif marco_2_rect_lose.collidepoint(event.pos):
                        nivel_1()
                
                if music_button_rect.collidepoint(mouse_pos):
                    toggle_music()
                    if music_playing:
                        music_button_img = music_on_img
                    else:
                        music_button_img = music_off_img

        keys = pygame.key.get_pressed()
        delta_ms = clock.tick(FPS)
        score_timer += delta_ms
        elapsed_time += delta_ms / 2000

        #Declaracion del fondo del juego
        screen.blit(imagen_fondo, (0, 0))

        #Dibujas en pantalla objetos variados
        for plataforma in plataformas:
            plataforma.draw(screen)

        for index, enemy in enumerate(enemy_list):
                enemy.update(delta_ms, plataformas, enemy_list, index, pause=player_1.pause)
                enemy.draw(screen)

                if not player_1.pause:
                    enemy.objetos_lanzados.update()
                enemy.objetos_lanzados.draw(screen)

        for index, enemy_2 in enumerate(enemy_list_2):
            enemy_2.update(delta_ms, enemy_list_2, index=index, pause=player_1.pause)
            enemy_2.draw(screen)

            if not player_1.pause:
                    enemy_2.objetos_lanzados.update()
            enemy_2.objetos_lanzados.draw(screen)
            
        for pinches in trampas_list:
            pinches.draw(screen)

        for obj in estrella:
            obj.update(delta_ms)
            rotated_image = pygame.transform.rotate(obj.image, obj.angle)
            rotated_rect = rotated_image.get_rect(center=obj.rect.center)
            screen.blit(rotated_image, rotated_rect)
        
        for i in poder:
            i.update(delta_ms)
            rotated_image = pygame.transform.rotate(i.image, i.angle)
            rotated_rect = rotated_image.get_rect(center=i.rect.center)
            screen.blit(rotated_image, rotated_rect)
        
        if player_1.lives > 0 and player_1.pause==False and player_1.game_over==False:
            if score_timer >= 2000: 
                player_1.score += 2
                score_timer = 0 

        if player_1.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - player_1.invulnerable_timer >= player_1.invulnerable_duration:
                player_1.invulnerable = False  

        if player_1.win or time_limit == 0 or player_1.pause == True or player_1.game_over==True:
            if time_limit == 0:
                player_1.game_over = True
        else:
            # Actualizar el cronómetro
            elapsed_time += delta_ms / 2000 
            if elapsed_time >= 1:
                time_limit -= 1
                elapsed_time = 0

        #Dibujo en pantalla de actualizaciones de personaje, plataforma, etc
        player_1.events(delta_ms, keys)
        player_1.update(delta_ms, plataformas, player_1, index, enemy_list, enemy_list_2, plataforma_movil_lista=None)
        player_1.draw(screen)
        
        player_1.objetos_lanzados.update()
        player_1.objetos_lanzados.draw(screen)

        #Texto en pantalla de vida, puntaje y estrellas recogidas
        font=pygame.font.SysFont("arial", 20, True)

        font_score=pygame.font.SysFont("comicsans", 20, True)
        score_text = font_score.render("Score: " + str(player_1.score), True, (255, 255, 255))
        screen.blit(score_text, (600, 5))

        lives_text = font.render("Lives:", True, (255, 255, 255))
        screen.blit(lives_text, (10, 5))

        stars_text = font.render("Stars:", True, (255, 255, 255))
        screen.blit(stars_text, (300, 5))

        font_path = "fonts/LLPIXEL3.ttf"
        font_size = 20
        font_timer = pygame.font.Font(font_path, font_size) 
        text_time = font_timer.render("Time:"+str(time_limit), True, (255, 255, 255))
        screen.blit(text_time, (800, 5))

        marco_1_rect=None
        marco_2_rect=None
        marco_3_rect=None


        if player_1.pause and not player_1.win:
            marco = pygame.image.load("images/gui/set_gui_01/Comic/menu/espacio.jpg")
            marco = pygame.transform.scale(marco, (600, 500))  
            marco_rect = marco.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

            pause_image=pygame.image.load("images/gui/set_gui_01/Large Buttons/Header.png")
            pause_image=pygame.transform.scale(pause_image, (300, 100))  
            pause_rect=pygame.Rect((ANCHO_VENTANA //2 -150, ALTO_VENTANA //2 -300, 90, 90))

            marco_1_image = pygame.image.load("images/gui/set_gui_01/Large Buttons/Continue Button.png")
            marco_1_image = pygame.transform.scale(marco_1_image, (300, 100))
            marco_1_rect = pygame.Rect(ANCHO_VENTANA //2- 130, ALTO_VENTANA //2 -170, 290, 90)  

            marco_2_image = pygame.image.load("images/gui/set_gui_01/Large Buttons/New game Button.png")
            marco_2_image = pygame.transform.scale(marco_2_image, (300, 100))
            marco_2_rect = pygame.Rect(ANCHO_VENTANA //2 - 130, ALTO_VENTANA //2 -40, 290, 90)  

            marco_3_image = pygame.image.load("images/gui/set_gui_01/Large Buttons/Menu Button.png")
            marco_3_image = pygame.transform.scale(marco_3_image, (300, 100))
            marco_3_rect = pygame.Rect(ANCHO_VENTANA //2 -130, ALTO_VENTANA //2 +100, 290, 90)  

            font_score=pygame.font.SysFont("comicsans", 20, True)
            score_text = font_score.render("Score: " + str(player_1.score), True, (255, 255, 255))
            score_rect = pygame.Rect(ANCHO_VENTANA //2 - 150, ALTO_VENTANA //2 -100, 90, 90)

            music_on_img = pygame.image.load("images/gui/set_gui_01/Comic/Buttons/audioPlus.png")
            music_off_img = pygame.image.load("images/gui/set_gui_01/Comic/Buttons/audioMute.png")


            if music_playing:
                music_button_img = music_on_img
            else:
                music_button_img = music_off_img

            music_button_rect = pygame.Rect(ANCHO_VENTANA // 2 - 250, ALTO_VENTANA // 2 + 100, 90, 90)

            screen.blit(score_text, score_rect)
            screen.blit(marco, marco_rect)
            screen.blit(pause_image, pause_rect)
            screen.blit(marco_1_image, marco_1_rect)
            screen.blit(marco_2_image, marco_2_rect)
            screen.blit(marco_3_image, marco_3_rect)
            screen.blit(music_button_img, music_button_rect)
        
        marco_1_rect_win=None
        marco_2_rect_win=None
        marco_3_rect_win=None

        if player_1.win:
            marco_win = pygame.image.load("images/gui/set_gui_01/Comic/menu/space.jpg")
            marco_win = pygame.transform.scale(marco_win, (600, 500))  
            marco_rect_win = marco_win.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

            text_level_win=pygame.image.load("images/gui/set_gui_01/Large Buttons/win.png")
            text_level_win = pygame.transform.scale(text_level_win, (300, 100))
            text_win_rect = pygame.Rect(ANCHO_VENTANA //2 -150, ALTO_VENTANA //2 -190, 90, 90) 

            marco_1_image_win = pygame.image.load("images/gui/set_gui_01/option buttons/Return Square Button.png")
            marco_1_image_win = pygame.transform.scale(marco_1_image_win, (100, 100))
            marco_1_rect_win = pygame.Rect(ANCHO_VENTANA //2 -250, ALTO_VENTANA //2 +100, 90, 90) 

            marco_2_image_win = pygame.image.load("images/gui/set_gui_01/option buttons/Home Square Button.png")
            marco_2_image_win = pygame.transform.scale(marco_2_image_win, (100, 100))
            marco_2_rect_win = pygame.Rect(ANCHO_VENTANA //2 - 40, ALTO_VENTANA //2 +100, 90, 90) 

            marco_3_image_win = pygame.image.load("images/gui/set_gui_01/option buttons/Next Square Button.png")
            marco_3_image_win = pygame.transform.scale(marco_3_image_win, (100, 100))
            marco_3_rect_win = pygame.Rect(ANCHO_VENTANA //2 +150, ALTO_VENTANA //2 +100, 90, 90) 

            font_score=("fonts/Symtext.ttf")
            font_size = 30
            score_size = pygame.font.Font(font_score, font_size)
            
            score_text = score_size.render("Your Score: " + str(player_1.score), True, (0, 0, 0))
            score_rect = pygame.Rect(ANCHO_VENTANA //2 - 140, ALTO_VENTANA //2, 90, 90)

            screen.blit(marco_win, marco_rect_win)
            screen.blit(text_level_win, text_win_rect)
            screen.blit(marco_1_image_win, marco_1_rect_win)
            screen.blit(marco_2_image_win, marco_2_rect_win)
            screen.blit(marco_3_image_win, marco_3_rect_win)
            screen.blit(score_text, score_rect)
        
        marco_1_rect_lose=None
        marco_2_rect_lose=None

        if player_1.game_over:
            marco_lose = pygame.image.load("images/gui/set_gui_01/Comic/menu/space.jpg")
            marco_lose = pygame.transform.scale(marco_lose, (600, 500))
            marco_rect_lose = marco_lose.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

            text_level_lose=pygame.image.load("images/gui/set_gui_01/Large Buttons/lose.png")
            text_level_lose = pygame.transform.scale(text_level_lose, (300, 100))
            text_lose_rect = pygame.Rect(ANCHO_VENTANA //2 -150, ALTO_VENTANA //2 -190, 90, 90) 

            marco_1_image_lose = pygame.image.load("images/gui/set_gui_01/option buttons/Home Square Button.png")
            marco_1_image_lose = pygame.transform.scale(marco_1_image_lose, (100, 100))
            marco_1_rect_lose = pygame.Rect(ANCHO_VENTANA //2 -250, ALTO_VENTANA //2 +100, 90, 90) 

            marco_2_image_lose = pygame.image.load("images/gui/set_gui_01/option buttons/Return Square Button.png")
            marco_2_image_lose = pygame.transform.scale(marco_2_image_lose, (100, 100))
            marco_2_rect_lose = pygame.Rect(ANCHO_VENTANA //2 +150, ALTO_VENTANA //2 +100, 90, 90) 

            font_score=("fonts/Symtext.ttf")
            font_size = 30
            score_size = pygame.font.Font(font_score, font_size)
            
            score_text = score_size.render("Your Score: " + str(player_1.score), True, (0, 0, 0))
            score_rect = pygame.Rect(ANCHO_VENTANA //2 - 140, ALTO_VENTANA //2, 90, 90)

            screen.blit(marco_lose, marco_rect_lose)
            screen.blit(text_level_lose, text_lose_rect)
            screen.blit(marco_1_image_lose, marco_1_rect_lose)
            screen.blit(marco_2_image_lose, marco_2_rect_lose)
            screen.blit(score_text, score_rect)

        pygame.display.flip()