import pygame
from time import sleep

pygame.init()

antalrader = 30
antalkolumner = 30
skärm = pygame.display.set_mode((antalkolumner*16+1,antalrader*16+1))

färg = ()   # Variabel som antingen antar vit eller blå
vit = (255,255,255)
blå = (0,0,255)

rad = []    # En rad med vågor
rad0 = []   # Raden med kolumnernas namn
jämför = [] # Bräde för "cellanalys"

bräde = []

# Skapar en rad med vågor
for k in range(antalkolumner):
    rad.append("~")

# Skapar båtbrädet av vågorna
for r in range (antalrader):  # Sätter in raderna i brädet
    bräde.append(list(rad))

def rita_bräde():
    for rindex in range(antalrader):
        for kindex in range(antalkolumner):
            if bräde[rindex][kindex] == "X":
                färg = blå
            else:
                färg = vit
            pygame.draw.rect(skärm, färg, ((1+kindex*16, 1+rindex*16),(15,15)))
    pygame.display.flip()

klar = False
while not klar: # Val av koordinater
    rita_bräde()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = list(pygame.mouse.get_pos())
                pos[0] = (pos[0]-1)//16
                pos[1] = (pos[1]-1)//16
                if bräde[pos[1]][pos[0]] == "~":
                    bräde[pos[1]][pos[0]] = "X"
                else:
                    bräde[pos[1]][pos[0]] = "~"    
            elif event.button == 3:
                klar = True

# Körning av det huvudsakliga "spelet"
while True:
    rita_bräde()
    jämför = []
    for r in range(0, antalrader):
        jämför.append([])
        for k in range(0, antalkolumner):
            jämför[r].append(bräde[r][k])
    for cellr in range(0, antalrader):
        for cellk in range(0, antalkolumner):
            grannar = 0     # Räknar antalet grannar om cellen är "~" eller antalet grannar +1 om cellen är "X"
            for radindex in range(cellr-1, cellr+2): # Radindex som eventuellt ska undersökas
                if 0 <= radindex < antalrader:  # Kollar enbart de radindex som faktiskt finns (då en cell kan ligga intill en kant)
                    for kolumnindex in range(cellk-1, cellk+2): # Kolumnindex -||-
                        if 0 <= kolumnindex < antalkolumner: # Kollar enbart de kolumnindex som faktiskt finns (-||-)
                            if jämför[radindex][kolumnindex] == "X":
                                grannar += 1
            if jämför[cellr][cellk] == "~" and grannar == 3:
                bräde[cellr][cellk] = "X"
            if jämför[cellr][cellk] == "X":
                grannar -= 1
                if grannar<2 or grannar>3:
                    bräde[cellr][cellk] = "~"
    sleep(0.5)








