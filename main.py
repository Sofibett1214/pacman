import pygame
import sys
from constantes import *
from juego import Juego 

def main():
    try:
        #inicializar pygame
        pygame.init()

        juego = Juego()
        juego.run()

    except Exception as e:
        print (f"Error: {e}")
        sys.exit(1)
    finally: 
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
    
