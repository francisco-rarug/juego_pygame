import pygame
from constantes import *
from auxiliar import Auxiliar
from objeto import *

class Enemy_2(pygame.sprite.Sprite):
    def __init__(self, x, y, p_scale=1, numero_enemy_2=None):
        super().__init__()

        # self.shoot= Auxiliar.getSurfaceFromSeparateFiles("images/npc/{0}.png", 1, 4, scale=p_scale)
        self.lives=2
        self.numero_enemy_2=numero_enemy_2
        if self.numero_enemy_2==1:
            self.animation= Auxiliar.getSurfaceFromSeparateFiles("images/npc/npc_2/{0}.png", 1, 4, scale=p_scale)
        elif self.numero_enemy_2==2:
            
            self.animation= Auxiliar.getSurfaceFromSeparateFiles("images/npc/{0}.png", 1, 4, scale=p_scale)
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_visible = True
        self.dead_r=Auxiliar.getSurfaceFromSpriteSheet("images/npc/die/1.png", 6, 1, scale=p_scale)[1:6]
        if self.numero_enemy_2==1:
            self.direction = DIRECTION_L

        if self.numero_enemy_2==2:
            self.direction = DIRECTION_R

        self.ataque = False
        self.objetos_lanzados = pygame.sprite.Group()
        self.attack_cooldown = 7000 
        self.last_attack_time = pygame.time.get_ticks()
        self.is_dead = False

        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.frame_rate_ms = 200  # Ajusta este valor para ralentizar la animación

        self.tiempo_transcurrido_animation = 0
    

    def animate(self, delta_ms, enemy_list_2, index):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            self.frame += 1
            if self.frame >= len(self.animation)-1:
                if self.animation==self.dead_r:
                    del enemy_list_2[index]
                else:
                    self.frame = 0
            self.image = self.animation[self.frame]

    def death_animation(self):
        self.is_dead = True
        if self.direction == DIRECTION_R:
            self.animation = self.dead_r
        else:
            self.direction == DIRECTION_L
            self.animation = self.dead_r

    def puede_atacar(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time
        return elapsed_time >= self.attack_cooldown

    def lanzar_objeto(self):
        objeto = Objeto(self.rect.centerx, self.rect.centery, self.direction, self, p_scale=0.4, numero_objeto=1)

        if self.direction == DIRECTION_R:
            objeto.velocidad_x = objeto.velocidad
        else:
            objeto.velocidad_x = -objeto.velocidad

        self.objetos_lanzados.add(objeto)


    def atacar(self, pause):
        if not pause:
            if self.puede_atacar():
                self.lanzar_objeto()
                self.last_attack_time = pygame.time.get_ticks()

                sonido_colision = pygame.mixer.Sound("audio/shoot_enemy_2.mp3")
                volumen = 0.2 
                sonido_colision.set_volume(volumen)
                sonido_colision.play()

    def update(self, delta_ms, enemy_list_2, index, pause):
        if not pause:
            self.animate(delta_ms, enemy_list_2, index)
            self.atacar(pause)

    def draw(self, screen):
        if self.is_visible:
            if(DEBUG):
                pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
                pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
            
            self.image = self.animation[self.frame]
            screen.blit(self.image,self.rect)

    def receive_shoot(self, enemy_list_2):
        self.lives -= 1
        print(self.lives)
        if self.lives <= 0:
            self.lives = 0
            self.death_animation()
            
            sonido_colision = pygame.mixer.Sound("audio/dead_enemy.mp3")
            volumen = 0.2 
            sonido_colision.set_volume(volumen)
            sonido_colision.play()

            enemy_list_2.remove(self)


