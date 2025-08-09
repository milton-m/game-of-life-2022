import pygame
from time import sleep

pygame.init()

ANTALRADER = 200    # Antal rader och kolumner i brädet
ANTALKOLUMNER = 200 
startr = 130        # Start- och slutvärdena för raderna respektive kolumnerna som ska ritas ut i Pygame-fönstret
slutr = 169
startk = 130
slutk = 169

startskärm1 = pygame.image.load("startskärm1.png")
startskärm2 = pygame.image.load("startskärm2.png")
spela_svart = pygame.image.load("spela_svart.png")
spela_blå = pygame.image.load("spela_blå.png")
icon = pygame.image.load("icon.png")

färg = ()   # Tupel som antar en viss färg
VIT = (255,255,255)
SVART = (0,0,0)
GRÅ = (100,100,100)
RÖD = (255,0,0)
BLÅ = (0,0,255)
LJUSBLÅ = (200,200,255)

textinfo = pygame.font.SysFont("times new roman", 29)

rad = []    # En rad med vågor

bräde = []
jämför = [] # "Mallbräde" under generationsbyte
uppställ = [] # Bräde som sparar det uppställda brädet
urklipp = [] # Bräde där användaren kan spara en del av det uppställda brädet för kopiering

pos = ()    # Variabel som tar emot musposition
posi = ()   # Index (både för kolumn och rad) för en ruta för en musposition
s_pos = ()  # Motsvarande pos som användes för att använda startpositionen under mask-kopiering av celler
s_posi = ()

iterationer = 0

def rita_bräde():
    skärm.fill(SVART)
    for r in range(startr, slutr+1):
        for k in range(startk, slutk+1):
            if bräde[r][k] == "X":
                if paus:
                    färg = GRÅ
                else:
                    färg = BLÅ
            else:
                färg = VIT
            pygame.draw.rect(skärm, färg, (1+(k-startk)*16, 1+(r-startr)*16, 15 ,15))
            
    if uppställning == False:
        textyta = textinfo.render((' Iteration ' + str(iterationer) + " "), True, VIT, SVART)
        skärm.blit(textyta, (0,0))

def listkopiator(kop_lista, ref_lista): # Kopierar över ref_lista till kop_lista
    kop_lista.clear()   # Sätter kop_lista till [] (använder ej kop_lista = [] pga av att det då defineras en ny lista).
    for r in range(0, ANTALRADER):
        kop_lista.append([])
        for k in range(0, ANTALKOLUMNER):
            kop_lista[r].append(ref_lista[r][k])

def generationsbyte():
    listkopiator(jämför, bräde)
    for cellr in range(0, ANTALRADER):
        for cellk in range(0, ANTALKOLUMNER):
            grannar = 0     # Räknar antalet grannar om cellen är "~" eller antalet grannar +1 om cellen är "X"
            for radindex in range(cellr-1, cellr+2): # Radindex som eventuellt ska undersökas
                if 0 <= radindex < ANTALRADER: # Kollar enbart de radindex som faktiskt finns (då en cell kan ligga vid en kant)
                    for kolumnindex in range(cellk-1, cellk+2): # Kolumnindex -||-
                        if 0 <= kolumnindex < ANTALKOLUMNER: # Kollar enbart de kolumnindex som faktiskt finns (-||-)
                            if jämför[radindex][kolumnindex] == "X":
                                grannar += 1
            if jämför[cellr][cellk] == "~" and grannar == 3:
                bräde[cellr][cellk] = "X"
            elif jämför[cellr][cellk] == "X":
                if grannar<3 or grannar>4:  # grannar är antalet närliggande celler +1
                    bräde[cellr][cellk] = "~"
    #sleep(0.05)

# Skapar en rad med vågor
for k in range(ANTALKOLUMNER):
    rad.append("~")

# Skapar båtbrädet av vågorna
for r in range (ANTALRADER):  # Sätter in raderna i brädet
    bräde.append(list(rad))


skärm = pygame.display.set_mode((1282,641))
pygame.display.set_caption("Conway's Game of Life")
pygame.display.set_icon(icon)
meny = True # Variabel för pågående meny
spelar = True # Variabel för pågående spel
animering = 0 # Variabel för "cellanimation" i menyn

while meny:
    animering += 0.1
    if int(animering)%2:
        skärm.blit(startskärm1, (0,0))
    else:
        skärm.blit(startskärm2, (0,0))
    pos = pygame.mouse.get_pos()
    if 514<pos[0]<768 and 309<pos[1]<434:
        skärm.blit(spela_blå, (515,310))
    else:
        skärm.blit(spela_svart, (515,310))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            meny = False
            spelar = False
        elif 514<pos[0]<768 and 309<pos[1]<434 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                meny = False

    pygame.display.flip()

pygame.display.quit() #??? RADERAR SKÄRM-INSTÄLLNINGARNA?

skärm = pygame.display.set_mode(((slutk-startk+1)*16+1,(slutr-startr+1)*16+1))
pygame.display.set_caption("Conway's Game of Life")
pygame.display.set_icon(icon)
uppställning = True
paus = False
välj_mask = False # Variabel för pågående "maskning"
while spelar:
    rita_bräde()
    if välj_mask == True:
        pos = pygame.mouse.get_pos()
        posi = [(pos[0]-1)//16+startk, (pos[1]-1)//16+startr]
        for r in range(min(posi[1], s_posi[1]), max(posi[1], s_posi[1])+1):
            for k in range(min(posi[0], s_posi[0]), max(posi[0], s_posi[0])+1):
                if bräde[r][k] == "X":
                    färg = SVART
                else:
                    färg = LJUSBLÅ
                pygame.draw.rect(skärm, färg, (1+(k-startk)*16, 1+(r-startr)*16, 15 ,15))

        pygame.draw.rect(skärm, RÖD, (min(s_pos[0], pos[0]), min(s_pos[1], pos[1]),
                                        abs(s_pos[0]-pos[0]), abs(s_pos[1]-pos[1])), 2)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            spelar = False
        if event.type == pygame.KEYDOWN and välj_mask == False:
            if event.key == pygame.K_UP and startr != 0:
                startr -= 1
                slutr -= 1
            if event.key == pygame.K_DOWN and slutr != ANTALRADER - 1:
                startr += 1
                slutr += 1
            if event.key == pygame.K_LEFT and startk != 0:
                startk -= 1
                slutk -= 1
            if event.key == pygame.K_RIGHT and slutk != ANTALKOLUMNER - 1:
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
                    posi = list(pygame.mouse.get_pos())
                    posi[0] = (posi[0]-1)//16+startk
                    posi[1] = (posi[1]-1)//16+startr
                    if bräde[posi[1]][posi[0]] == "~":
                        bräde[posi[1]][posi[0]] = "X"
                    else:
                        bräde[posi[1]][posi[0]] = "~"
                elif event.button == 3:
                    s_pos = pygame.mouse.get_pos()
                    s_posi = [(s_pos[0]-1)//16+startk, (s_pos[1]-1)//16+startr]
                    välj_mask = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                välj_mask = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and välj_mask == False:
                    listkopiator(uppställ, bräde)
                    uppställning = False

                elif välj_mask:
                    if event.key == pygame.K_c:
                        urklipp = []
                        for r in range(min(posi[1], s_posi[1]), max(posi[1], s_posi[1])+1):
                            urklipp.append([])
                            for k in range(min(posi[0], s_posi[0]), max(posi[0], s_posi[0])+1):
                                urklipp[r - min(posi[1], s_posi[1])].append(bräde[r][k])
                    elif event.key == pygame.K_BACKSPACE:
                        for r in range(min(posi[1], s_posi[1]), max(posi[1], s_posi[1])+1):
                            for k in range(min(posi[0], s_posi[0]), max(posi[0], s_posi[0])+1):
                                bräde[r][k] = "~"
                elif event.key == pygame.K_v:
                    posi = list(pygame.mouse.get_pos())
                    posi[0] = (posi[0]-1)//16+startk
                    posi[1] = (posi[1]-1)//16+startr
                    for r in range(len(urklipp)):
                        for k in range(len(urklipp[r])):
                            if r+posi[1] < ANTALRADER and k+posi[0] < ANTALKOLUMNER:
                                bräde[r+posi[1]][k+posi[0]] = urklipp[r][k]

    if uppställning == False and paus == False:
        generationsbyte()
        iterationer += 1

pygame.quit()






