import os
from time import sleep

antalrader = 20
antalkolumner = 20

rad = []    # En rad med vågor
rad0 = []   # Raden med kolumnernas namn
jämför = [] # Bräde för "cellanalys"

bräde = []

# Skapar en rad med vågor
for k in range(antalkolumner):
    rad.append("~")

# Skapar båtbrädet av vågorna
for r in range (antalrader):  # Sätter in raderna i brädena
    bräde.append(list(rad))  
                                
# Skapar raden med kolumnernas namn
for unicode in range(ord('A'),ord('A')+antalkolumner):
    rad0.append(chr(unicode))

def rita_bräde():
    for rindex in range(antalrader):
        for k in bräde[rindex]:
            print(k, end=" ") # ,end="" för att print ska fortsätta skriva i samma rad
        print() # För att skriva på nästa rad

klar = False
while not klar:
    sökning = True
    while sökning:      # Genomsökande av giltlig koordinat
        rita_bräde()
        s_koordinat = input('\nVilket koordinat ska en cell utplaceras på (skriv "klar" om du är klar)? ')
        if s_koordinat.upper() == "KLAR":
            klar = True
            break
        s_koordinat = s_koordinat.split(";")   # Översätter koordinaten till en lista med tal
        s_koordinat[0] = int(s_koordinat[0])
        s_koordinat[1] = int(s_koordinat[1])
        if bräde[s_koordinat[1]][s_koordinat[0]] == "~":
            bräde[s_koordinat[1]][s_koordinat[0]] = "X"
        else:
            bräde[s_koordinat[1]][s_koordinat[0]] = "~"
        os.system('cls')
        
# Körning av det huvudsakliga "spelet"
while True:
    os.system('cls')
    rita_bräde()
    jämför = []
    for r in range(0, 20):
        jämför.append([])
        for k in range(0, 20):
            jämför[r].append(bräde[r][k])
    for cellr in range(0, 20):
        for cellk in range(0, 20):
            grannar = 0     # Räknar antalet grannar om cellen är "~" eller antalet grannar +1 om celler är "X"
            for radindex in range(cellr-1, cellr+2): # Radindex som eventuellt ska undersökas
                if 0 <= radindex <= 19:  # Kollar enbart de radindex som faktiskt finns (då en cell kan ligga intill en kant)
                    for kolumnindex in range(cellk-1, cellk+2): # Kolumnindex -||-
                        if 0 <= kolumnindex <= 19: # Kollar enbart de kolumnindex som faktiskt finns (-||-)
                            if jämför[radindex][kolumnindex] == "X":
                                grannar += 1
            if jämför[cellr][cellk] == "~" and grannar == 3:
                bräde[cellr][cellk] = "X"
            if jämför[cellr][cellk] == "X":
                grannar -= 1
                if grannar<2 or grannar>3:
                    bräde[cellr][cellk] = "~"
    sleep(0.5)








