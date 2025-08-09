# Bubble sort

"""
lista = [435,12,4,3234,5,423,12,4,3123]
n_klar = 0
färdig = False
temp = 0

while not färdig:
    färdig = True
    for v_index in range(len(lista)-1-n_klar):
        if lista[v_index] > lista[v_index+1]:
            temp = lista[v_index]
            lista[v_index] = lista[v_index+1]
            lista[v_index+1] = temp
            färdig = False
print(lista)
"""

# Selection sort

"""
lista = [546,213,578,24,6,1,6,123,8,34,8,123]

for i in range(len(lista)-1):
    m_index = i
    for j in range(i+1, len(lista)):
        if lista[j] < lista[m_index]:
            m_index = j
    lista.insert(i, lista[m_index])
    lista.pop(m_index+1)

print(lista)
"""

# Insertion sort

"""
lista = [43,8,12,88,12,6,8,211,664,223,1234]

for i in range(1,len(lista)):
    for j in range(0,i):
        if lista[i] < lista[j]:
            lista.insert(j, lista[i])
            lista.pop(i+1)
            break
print(lista)
"""

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
    for bokstav in rad0:
        if bokstav == "A":      # Gör så att "bokstavsindexeringen" börjar först tre rutor in
            print(end="   ")
        print(bokstav, end=" ")
    print()
    for rindex in range(antalrader):
        print(rindex+1, end=" ")
        if rindex < 9:     # Gör så att rutorna avsedda att vara i samma kolumn inte förskjuts
            print(end=" ")
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
        s_koordinat = [s_koordinat[0],s_koordinat.replace(s_koordinat[0],"")]   # Översätter koordinaten till en lista
        if not s_koordinat[0].upper() in rad0 or not s_koordinat[1].isdigit() or not int(s_koordinat[1]) in range(1,21): #...
            os.system('cls')
            print("Ogiltlig cell") # ...Om s_koordinat inte består av en kolumnbokstav och ett heltal 1-10 (i string-datatyp)...
            continue                 # ...(för att undvika en krasch)
        s_koordinat[0] = rad0.index(s_koordinat[0].upper()) # Kolumnbokstaven ersätts med index 0-9
        s_koordinat[1] = int(s_koordinat[1])-1      # Indexering 1-10 blir 0-9
        sökning = False
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
                if 0 <= radindex <= 19:  # Kollar enbart de radindex som faktiskt finns (då en båt kan ligga intill en kant)
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








