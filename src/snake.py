# Snake the videogame coded with python run on pygame
# 
# Autors : Jakub Zak
# Colaborators : Jakub Senkyr
#
# Version : 0.0
# adding pygame
import sys

import pygame
pygame.init()

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            
            # adding ability to turn this game off
            pygame.quit()
            sys.exit()

    keyword_pressed = pygame.key.get_pressed()        

    # backround
    okno.fill((255, 255, 255))
    
    pygame.display.update()