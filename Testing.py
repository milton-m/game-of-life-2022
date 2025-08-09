import pygame

pygame.init()

skärm = pygame.display.set_mode((300,300))

minfont = pygame.font.SysFont("times new roman", 30)
textyta = minfont.render('Hello World!', False, (255,255,255))

skärm.blit(textyta, (0,0))
pygame.display.flip()
