import pygame

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
ikon = pygame.image.load("ikon.png")

färg = ()   # Tupel som antar en viss färg
cfärg = ()  # Tupel (för cellfärg) som antar antingen GRÅ resp. BLÅ nedan beroende på om spelet är pausat resp. igång/uppställning
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

nedsaktning = 0 # Variabel för "cellanimation" i menyn och för nedsaktning av generationsbytet
iterationer = 0

def rita_bräde():
    skärm.fill(SVART)
    if paus:
        cfärg = GRÅ
    else:
        cfärg = BLÅ
    for r in range(startr, slutr+1):
        for k in range(startk, slutk+1):
            if bräde[r][k] == "X":
                färg = cfärg
            else:
                färg = VIT
            pygame.draw.rect(skärm, färg, (1+(k-startk)*16, 1+(r-startr)*16, 15 ,15)) # Fyller i en ruta
            
    snabbhet_yta = textinfo.render((" " + läge.capitalize() + " "), True, VIT, SVART)
    skärm.blit(snabbhet_yta, (0,0)) # Skriver ut hastigheten för generationsbytet
    if uppställning == False:
        iteration_yta = textinfo.render((" Iteration " + str(iterationer) + " "), True, VIT, SVART)
        skärm.blit(iteration_yta, (0,32)) # Skriver ut antalet iterationer

def listkopiator(kop_lista, ref_lista): # Kopierar över ref_lista till kop_lista
    kop_lista.clear()   # Sätter kop_lista till [] (använder ej kop_lista = [] pga av att det då defineras en ny lista).
    for r in range(ANTALRADER):
        kop_lista.append([])
        for k in range(ANTALKOLUMNER):
            kop_lista[r].append(ref_lista[r][k])

def generationsbyte():
    listkopiator(jämför, bräde)
    for cellr in range(ANTALRADER):
        for cellk in range(ANTALKOLUMNER):
            grannar = 0     # Räknar antalet grannar om rutan är "~" (tom) eller antalet grannar +1 om rutan är "X" (cell)
            for radindex in range(cellr-1, cellr+2): # Radindex som eventuellt ska undersökas
                if 0 <= radindex < ANTALRADER: # Kollar enbart de radindex som faktiskt finns (då en cell kan ligga vid en kant)
                    for kolumnindex in range(cellk-1, cellk+2): # Kolumnindex -||-
                        if 0 <= kolumnindex < ANTALKOLUMNER: # Kollar enbart de kolumnindex som faktiskt finns (-||-)
                            if jämför[radindex][kolumnindex] == "X":
                                grannar += 1
            if jämför[cellr][cellk] == "~" and grannar == 3:
                bräde[cellr][cellk] = "X"
            elif jämför[cellr][cellk] == "X" and (grannar<3 or grannar>4):  # grannar är antalet närliggande celler +1
                bräde[cellr][cellk] = "~"

# Skapar en rad med vågor
for k in range(ANTALKOLUMNER):
    rad.append("~")

# Skapar brädet av vågorna
for r in range (ANTALRADER):  # Sätter in raderna i brädet
    bräde.append(list(rad))

skärm = pygame.display.set_mode((1282,641))
pygame.display.set_caption("Conway's Game of Life")
pygame.display.set_icon(ikon)

meny = True # Variabel för pågående meny
spelar = True # Variabel för pågående spel
while meny:
    nedsaktning += 0.1
    if int(nedsaktning)%2: # int(nedsaktning) är nedsaktning "nedrundat" till närmaste heltal. Om jämnt så startskärm1
        skärm.blit(startskärm1, (0,0))
    else:               # annars (om udda) så startskärm2 
        skärm.blit(startskärm2, (0,0))
    pos = pygame.mouse.get_pos()
    if 514<pos[0]<768 and 309<pos[1]<434: # Om inom "spela"-rutan
        skärm.blit(spela_blå, (515,310))
    else:
        skärm.blit(spela_svart, (515,310))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            meny = False
            spelar = False
        elif 514<pos[0]<768 and 309<pos[1]<434\
        and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Om muspekaren inom "spela"-rutan och vänsterklickning
            meny = False
    pygame.display.flip()

pygame.display.quit() # För att den nya skärmen nedan ska bli centrerad på datorskärmen
skärm = pygame.display.set_mode(((slutk-startk+1)*16+1,(slutr-startr+1)*16+1))
pygame.display.set_caption("Conway's Game of Life")
pygame.display.set_icon(ikon)

uppställning = True
paus = False
välj_mask = False # Variabel för pågående "maskning"
läge = "snabb" # Hastigheteten på generationsbytet. Antar "snabb", "medel" eller "sakta"
nedsaktning = 0 # Återställer nedsaktning
while spelar:
    rita_bräde()
    if välj_mask == True:
        pos = pygame.mouse.get_pos()
        posi = [(pos[0]-1)//16+startk, (pos[1]-1)//16+startr]
        for r in range(min(posi[1], s_posi[1]), max(posi[1], s_posi[1])+1): # Markerade rutors radindex
            for k in range(min(posi[0], s_posi[0]), max(posi[0], s_posi[0])+1): # Markerade rutors kolumnindex
                if bräde[r][k] == "X":
                    färg = SVART
                else:
                    färg = LJUSBLÅ
                pygame.draw.rect(skärm, färg, (1+(k-startk)*16, 1+(r-startr)*16, 15 ,15)) # Fyller i en markerad ruta

        pygame.draw.rect(skärm, RÖD, (min(s_pos[0], pos[0]), min(s_pos[1], pos[1]), # Ritar ut "maskens ändar"
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
            if event.key == pygame.K_s:
                if läge == "snabb":
                    läge = "medel"
                elif läge == "medel":
                    läge = "sakta"
                else:
                    läge = "snabb"
            if event.key == pygame.K_SPACE and uppställning == False:
                if paus == False:
                    paus = True
                else:
                    paus = False
            if event.key == pygame.K_u:
                nedsaktning = 0 # Återställer nedsaktning
                iterationer = 0 # Återställer antalet iterationer
                paus = False    # Om programmet skulle vara pausat vid återgången till uppställning
                uppställning = True
                listkopiator(bräde, uppställ)

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
                        if r+posi[1] < ANTALRADER:  # Kopiera bara in på radindex som faktiskt finns
                            for k in range(len(urklipp[r])):
                                if k+posi[0] < ANTALKOLUMNER: # Kopiera bara in på kolumnindex som faktiskt finns
                                    bräde[r+posi[1]][k+posi[0]] = urklipp[r][k]
    if uppställning == False and paus == False:
        nedsaktning += 1
        if läge == "snabb" or läge == "medel" and nedsaktning%100 == 0 or läge == "sakta" and nedsaktning%500 == 0:
            generationsbyte()
            iterationer += 1

pygame.quit()
