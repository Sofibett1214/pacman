import pygame
import sys 
from constantes import *
from personaje import *

class Juego: 
    def __init__(self):
        pygame.init()  # Asegurarse de que pygame está inicializado primero
        pygame.font.init()  # Inicializar específicamente el módulo de fuentes
    
      

        self.ventana = pygame.display.set_mode((ANCHO_VENTANA,  ALTO_VENTANA))
        pygame.display.set_caption("Pacman")

        #Reloj para controlar la velocidad del juego
        self.clock = pygame.time.Clock()

        self.running = True
        self.game_state = PLAYING

        self.celdas = []
        self.coins = []
        self.jugador = None
        self.ghost = []
        self.score = 0
        
        self.font = pygame.font.Font(None, 36)  # Mover esto después de la inicialización
        self.create_level()

    def create_level(self):
        for row_index, row in enumerate(LEVEL):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    self.celdas.append(Celda(col_index, row_index))
                elif cell == "0":
                    self.coins.append(Coin(col_index, row_index))
                elif cell == "P":
                    self.jugador = Jugador(col_index, row_index)
                elif cell == "R":
                    self.ghost.append(Ghost(col_index, row_index, "red"))
                elif cell == "B":
                    self.ghost.append(Ghost(col_index, row_index, "blue"))
                elif cell == "G":
                    self.ghost.append(Ghost(col_index, row_index, "green"))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if self.game_state == GAME_OVER:
            self.running = False

    def update(self):


        if self.game_state == PLAYING:
            self.jugador.update(self.celdas) 
            for ghost in self.ghost:
                ghost.update(self.celdas)   
                if self.jugador.rect.colliderect(ghost.rect):
                    self.game_state = GAME_OVER
                     
            for coin in self.coins[:]:
                coin.update()
                if self.jugador.rect.colliderect(coin.rect):
                    self.coins.remove(coin)
                    self.score += POINTS_PER_COIN

    def draw(self):
        self.ventana.fill(NEGRO)

        for celda in self.celdas:
            celda.draw(self.ventana)
        
        for coin in self.coins:
            coin.draw(self.ventana)

        self.jugador.draw(self.ventana)
        for ghost in self.ghost:
            ghost.draw(self.ventana)    

        score_text = self.font.render(f"Puntaje: {self.score}", True, BLANCO)
        self.ventana.blit(score_text, dest=(10, 10))

        pygame.display.update()
    
    def run(self):
        """Bucle prinicipal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60) 


if __name__ == "__main__":
    juego = Juego()
    juego.run()