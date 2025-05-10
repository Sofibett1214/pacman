from constantes import *
import pygame
import random 

class Celda:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x*CELDA_SIZE, y*CELDA_SIZE, CELDA_SIZE, CELDA_SIZE)

    def draw(self, ventana):
        pygame.draw.rect(ventana, PAREDES_COLOR, self.rect)

class Coin:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE + TILE_SIZE //2
        self.y = y * TILE_SIZE + TILE_SIZE //2
        try:
            self.personaje_sheet = pygame.image.load("assets/imagenes/BigCoin.png")
            if not self.personaje_sheet:
                raise FileNotFoundError("No se pudo cargar BigCoin.png")
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando BigCoin.png: {e}")
            self.personaje_sheet = pygame.Surface((16 * COIN_FRAMES, 16))
            self.personaje_sheet.fill((255, 255, 0))  # Color amarillo como fallback

        self.frames = []
        sheet_width = self.personaje_sheet.get_width()
        actual_frames = min(COIN_FRAMES, sheet_width // 16)
        
        for i in range(actual_frames):
            frame = pygame.Surface((16, 16), flags=pygame.SRCALPHA)
            frame.blit(self.personaje_sheet, dest=(0,0), area=(i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, size=(COIN_SIZE, COIN_SIZE))
            self.frames.append(frame)

        if not self.frames:  # Si no hay frames, crear al menos uno
            frame = pygame.Surface((COIN_SIZE, COIN_SIZE))
            frame.fill((255, 255, 0))  # Color amarillo como fallback
            self.frames.append(frame)

        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))
    def update(self): 
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > COIN_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % COIN_FRAMES
            self.animation_timer = current_time

        
    def draw(self, ventana):
        ventana.blit(self.frames[self.current_frame], self.rect)
        
class Ghost:
    def __init__(self, x, y, ghost_type):
        self.x = x * CELDA_SIZE + CELDA_SIZE // 2
        self.y = y * CELDA_SIZE + CELDA_SIZE // 2
        self.ghost_type = ghost_type
        self.speed = GHOST_SPEEDS[ghost_type]
        self.direction_change_time = GHOST_DIRECTION_TIMES[ghost_type]

        # Cargar la imagen correcta según el tipo de fantasma
        self.personaje_sheet = load_image(GHOST_SPRITES[ghost_type])
        self.frames = []
        for i in range(GHOST_ANIMATION_FRAMES):
            frame = pygame.Surface((16, 16), flags=pygame.SRCALPHA)
            frame.blit(self.personaje_sheet, dest=(0,0), area=(i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, size=(GHOST_SIZE, GHOST_SIZE))
            self.frames.append(frame)
        
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.direction = random.randint(0,3)
        self.direction_timer = pygame.time.get_ticks()
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))

    def can_move_in_direction(self, direction, paredes):
        dx = dy = 0
        if direction == DERECHA:
            dx = self.speed
        elif direction == IZQUIERDA:
            dx = -self.speed
        elif direction == ARRIBA:
            dy = -self.speed
        elif direction == ABAJO:
            dy = self.speed
        
        test_rect = self.rect.copy()
        test_rect.x += dx
        test_rect.y += dy
        
        for pared in paredes:
            if test_rect.colliderect(pared.rect):
                return False
        return True

    def change_direction(self, paredes):
        # Try all possible directions and choose a random valid one
        possible_directions = []
        for direction in [DERECHA, IZQUIERDA, ARRIBA, ABAJO]:
            if self.can_move_in_direction(direction, paredes):
                possible_directions.append(direction)
        
        if possible_directions:
            self.direction = random.choice(possible_directions)
        self.direction_timer = pygame.time.get_ticks()

    def move(self, paredes):
        current_time = pygame.time.get_ticks()
        if current_time - self.direction_timer > self.direction_change_time:
            self.change_direction(paredes)
        
        dx = dy = 0
        if self.direction == DERECHA:
            dx = self.speed
        elif self.direction == IZQUIERDA:
            dx = -self.speed
        elif self.direction == ARRIBA:
            dy = -self.speed
        elif self.direction == ABAJO:
            dy = self.speed


        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy
        can_move = True
        
        for pared in paredes:
            if new_rect.colliderect(pared.rect):
                can_move = False
                self.change_direction(paredes)
                break
        
        if can_move:
            self.x += dx
            self.y += dy
            self.rect.center = (self.x, self.y) 
      

    def update(self, paredes):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > GHOST_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % GHOST_ANIMATION_FRAMES  # Corregido: usando FRAMES en lugar de SPEED
            self.animation_timer = current_time

        self.move(paredes)
    def draw(self,ventana):
        ventana.blit(self.frames[self.current_frame],self.rect)







class Jugador: 
    def __init__(self, x, y):
        self.x = x * CELDA_SIZE + CELDA_SIZE // 2
        self.y = y * CELDA_SIZE + CELDA_SIZE // 2

        self.personaje_sheet = pygame.image.load("assets/imagenes/PacMan.png")

        #cargar todos los frames de animacion
        self.animation_frames = []
        for i in range(ANIMATION_FRAMES):
            #crear superficie para el frame
            frame = pygame.Surface((16, 16), pygame.SRCALPHA, 32)

            frame.blit(self.personaje_sheet, dest=(0, 0), area=pygame.Rect(i * 16, 0, 16, 16))
            #escalar el tamaño del jugador
            frame = pygame.transform.scale(frame, size=(JUGADOR_SIZE, JUGADOR_SIZE))
            self.animation_frames.append(frame)

        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.is_moving = False

        #imagen actual del jugador
        self.original_image = self.animation_frames[0]
        self.image = self.original_image


        self.rect = self.image.get_rect(center=(self.x,self.y))
        
        #direccion actual 
        self.direction = DERECHA
        #deltas
        self.dx = 0
        self.dy = 0

    
    def update_animation(self):
        if not self.is_moving:
            self.current_frame = 0
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > ANIMATION_VELOCIDAD:
            self.current_frame = (self.current_frame +1)% ANIMATION_FRAMES
            self.animation_timer = current_time

    def update_image(self):
        self.original_image = self.animation_frames[self.current_frame]
        

        if self.dx > 0:
            self.direction = DERECHA
            self.image = self.original_image
        elif self.dx < 0 :
            self.direction = IZQUIERDA #izquierda
            self.image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        elif self.dy < 0 :
            self.direction = ARRIBA
            self.image = pygame.transform.rotate(self.original_image, angle=90)
        elif self.dy > 0 :
            self.direction = ABAJO
            self.image = pygame.transform.rotate(self.original_image, angle=-90)
          

    
    def move(self, paredes):

        if self.dx != 0:
            if not self.check_collision(paredes, self.dx, 0):  # Corregido dy=0 a 0
                self.x += self.dx
            else:
                if self.check_collision(paredes, self.dx, -SLIDE_SPEED):
                    if not self.check_collision(paredes, self.dx, SLIDE_SPEED):
                        self.y += SLIDE_SPEED
                else:
                    self.y -= SLIDE_SPEED
        if self.dy != 0:
            if not self.check_collision(paredes, 0, self.dy):  # Corregido dx=0 a 0
                self.y += self.dy
            else:
                if self.check_collision(paredes, -SLIDE_SPEED, self.dy):
                    if not self.check_collision(paredes, SLIDE_SPEED, self.dy):
                        self.x += SLIDE_SPEED
                else:
                    self.x -= SLIDE_SPEED

        self.rect.center = (self.x, self.y)  # Actualizar la posición del rect






             

        #Actualizar posicion
        
        if self.x > ANCHO_VENTANA - JUGADOR_SIZE:
            self.x = 0
        elif self.x < 0:
            self.x = ANCHO_VENTANA - JUGADOR_SIZE

        if self.y > ALTO_VENTANA - JUGADOR_SIZE:
            self.y = 0
        elif  self.y < 0:
            self.y = ALTO_VENTANA - JUGADOR_SIZE

    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0

        if keys[pygame.K_RIGHT]:  # Antes: K_DERECHA
            self.dx = JUGADOR_VELOCIDAD
            self.direction = DERECHA
        elif keys[pygame.K_LEFT]:  # Antes: K_IZQUIERDA
            self.dx = -JUGADOR_VELOCIDAD
            self.direction = IZQUIERDA
        elif keys[pygame.K_UP]:  # Antes: K_ARRIBA
            self.dy = -JUGADOR_VELOCIDAD
            self.direction = ARRIBA
        elif keys[pygame.K_DOWN]:  # Antes: K_ABAJO
            self.dy = JUGADOR_VELOCIDAD
            self.direction = ABAJO
    
        #actualizar el estado de movimiento
        self.is_moving = self.dx != 0 or self.dy != 0
    def check_collision(self, celdas, dx=0, dy=0):
        future_rect = self.rect.copy()
        future_rect.x += dx
        future_rect.y += dy
    
        for pared in celdas:  # Cambiado walls por celdas
            if future_rect.colliderect(pared.rect):
                return True
        return False 




    def update(self, paredes):
        self.handle_input()
        self.update_animation()
        self.update_image()
        self.move(paredes)


        



        
    def draw(self, ventana):
        """Dibujar el jugador en la pantalla"""
        ventana.blit(self.image, self.rect)


    


    