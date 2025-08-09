import pygame
from time import sleep

pygame.init()

antalrader = 200
antalkolumner = 200
startr = 130
slutr = 169
startk = 130
slutk = 169
skärm = pygame.display.set_mode(((slutk-startk+1)*16+1,(slutr-startr+1)*16+1))

färg = ()   # Tupel som antingen antar vit eller blå
vit = (255,255,255)
blå = (0,0,255)
svart = (0,0,0)
grå = (100,100,100)
textinfo = pygame.font.SysFont("times new roman", 29)

rad = []    # En rad med vågor

bräde = []
jämför = [] # Bräde för "cellanalys"
uppställ = [] # Bräde som sparar det uppställda brädet

iterationer = 0

# Skapar en rad med vågor
for k in range(antalkolumner):
    rad.append("~")

# Skapar båtbrädet av vågorna
for r in range (antalrader):  # Sätter in raderna i brädet
    bräde.append(list(rad))

def rita_bräde():
    skärm.fill(svart)
    for rindex in range(startr, slutr+1):
        for kindex in range(startk, slutk+1):
            if bräde[rindex][kindex] == "X":
                if paus:
                    färg = grå
                else:
                    färg = blå
            else:
                färg = vit
            pygame.draw.rect(skärm, färg, ((1+(kindex-startk)*16, 1+(rindex-startr)*16),(15,15)))
            
    if uppställning == False:
        textyta = textinfo.render((' Iteration ' + str(iterationer) + " "), True, vit, svart)
        skärm.blit(textyta, (0,0))
    pygame.display.flip()

def listkopiator(kop_lista, ref_lista): # Kopierar över ref_lista till kop_lista
    kop_lista.clear()   # Sätter kop_lista till [] (använder ej kop_lista = [] pga av att det då defineras en ny lista).
    for r in range(0, antalrader):
        kop_lista.append([])
        for k in range(0, antalkolumner):
            kop_lista[r].append(ref_lista[r][k])

def generationsbyte():
    listkopiator(jämför, bräde)
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
            elif jämför[cellr][cellk] == "X":
                grannar -= 1
                if grannar<2 or grannar>3:
                    bräde[cellr][cellk] = "~"
    #sleep(0.05)

spelar = True
uppställning = True
paus = False
while spelar:
    rita_bräde()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            spelar = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and startr != 0:
                startr -= 1
                slutr -= 1
            if event.key == pygame.K_DOWN and slutr != antalrader - 1:
                startr += 1
                slutr += 1
            if event.key == pygame.K_LEFT and startk != 0:
                startk -= 1
                slutk -= 1
            if event.key == pygame.K_RIGHT and slutk != antalkolumner - 1:
                startk += 1
                slutk += 1
            if event.key == pygame.K_SPACE and uppställning == False:
                if paus == False:
                    paus = True
                else:
                    paus = False
            if event.key == pygame.K_u:
                iterationer = 0 # Återställer antalet iterationer
                paus = False    # Om programmet skulle vara pausat vid återgången till uppställning
                listkopiator(bräde, uppställ)
                uppställning = True

        if uppställning:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = list(pygame.mouse.get_pos())
                    pos[0] = (pos[0]-1)//16+startk
                    pos[1] = (pos[1]-1)//16+startr
                    if bräde[pos[1]][pos[0]] == "~":
                        bräde[pos[1]][pos[0]] = "X"
                    else:
                        bräde[pos[1]][pos[0]] = "~"    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                listkopiator(uppställ, bräde)
                uppställning = False
        
    if uppställning == False and paus == False:
        generationsbyte()
        iterationer += 1

pygame.quit()






