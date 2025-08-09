import pygame

pygame.init()

f_längd= 695
screen = pygame.display.set_mode((f_längd,f_längd))

for bkoord in range(5,f_längd-14,16):
    for hkoord in range(5,f_längd-14,16):
        pygame.draw.rect(screen, (255,255,255), ((bkoord, hkoord),(15,15)))
        
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(list(pygame.mouse.get_pos()))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Hello up")
            if event.key == pygame.K_RIGHT:
                print("Hello right")
    pygame.display.flip()
pygame.quit()
