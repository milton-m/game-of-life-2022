import pygame
from time import sleep
import os

pygame.init()

antalrader = 30
antalkolumner = 30
startr = 10
slutr = 19
startk = 10
slutk = 19
skärm = pygame.display.set_mode(((slutk-startk+1)*16+1,(slutr-startr+1)*16+1))

färg = ()   # Variabel som antingen antar vit eller blå
vit = (255,255,255)
blå = (0,0,255)

rad = []    # En rad med vågor
jämför = [] # Bräde för "cellanalys"

bräde = []

# Skapar en rad med vågor
for k in range(antalkolumner):
    rad.append("~")

# Skapar båtbrädet av vågorna
for r in range (antalrader):  # Sätter in raderna i brädet
    bräde.append(list(rad))

def rita_bräde():
    os.system("cls")
    for rindex in range(antalrader):
        for k in bräde[rindex]:
            print(k, end=" ") # ,end="" för att print ska fortsätta skriva i samma rad
        print() # För att skriva på nästa rad
    
    for rindex in range(startr, slutr+1):
        for kindex in range(startk, slutk+1):
            if bräde[rindex][kindex] == "X":
                färg = blå
            else:
                färg = vit
            pygame.draw.rect(skärm, färg, ((1+(kindex-startk)*16, 1+(rindex-startr)*16),(15,15)))
            pygame.display.flip()

klar = False
while not klar: # Val av koordinater
    rita_bräde()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                startr -= 1
                slutr -= 1
            if event.key == pygame.K_DOWN:
                startr += 1
                slutr += 1
            if event.key == pygame.K_LEFT:
                startk -= 1
                slutk -= 1
            if event.key == pygame.K_RIGHT:
                startk += 1
                slutk += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = list(pygame.mouse.get_pos())
                pos[0] = (pos[0]-1)//16+startk
                pos[1] = (pos[1]-1)//16+startr
                if bräde[pos[1]][pos[0]] == "~":
                    bräde[pos[1]][pos[0]] = "X"
                else:
                    bräde[pos[1]][pos[0]] = "~"    
            elif event.button == 3:
                klar = True

# Körning av det huvudsakliga "spelet"
while True:
    rita_bräde()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                startr -= 1
                slutr -= 1
            if event.key == pygame.K_DOWN:
                startr += 1
                slutr += 1
            if event.key == pygame.K_LEFT:
                startk -= 1
                slutk -= 1
            if event.key == pygame.K_RIGHT:
                startk += 1
                slutk += 1
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








