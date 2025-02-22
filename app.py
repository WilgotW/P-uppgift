from classes import * 
from roomGeneration import generateNodes
from gameLoop import startGame 
from globalVariables import *
from gui import *

def gameInstructions():
    print(
        """
        Du befinner dig i kulvertarna under D-huset, där den glupske Wumpus
        bor. För att undvika att bli uppäten måste du skjuta Wumpus med din
        pil och båge. Kulvertarna har 20 rum som är förenade med smala gångar.
        Du kan röra dig åt norr, öster, söder eller väster från ett rum till
        ett annat.

        Här finns dock faror som lurar. I vissa rum finns bottenlösa hål. Kliver
        du ner i ett sådant dör du omedelbart. I andra rum finns fladdermöss
        som lyfter upp dig, flyger en bit och släpper dig i ett godtyckligt
        rum. I ett av rummen finns Wumpus, och om du vågar dig in i det rummet
        blir du genast uppäten. Som tur är kan du från rummen bredvid känna
        vinddraget från ett avgrundshål eller lukten av Wumpus. Du får också
        i varje rum reda på vilka rum som ligger intill.

        För att vinna spelet måste du skjuta Wumpus. När du skjuter iväg en
        pil förflyttar den sig genom tre rum – du kan styra vilken riktning
        pilen ska välja i varje rum. Glöm inte bort att tunnlarna vindlar sig
        på oväntade sätt. Du kan råka skjuta dig själv…

        Lycka till!
        """
    )
    input("Tryck Enter för att fortsätta...")

def main():
    print("Välj svårighetsgrad:")
    print(
        """
        1. Lätt
        - Mindre hål och fladdermöss
        - 5 pilar

        2. Normal
        - Normalt många hål och fladdermöss
        - 5 pilar

        3. Svår
        - Fler hål och fladdermöss
        - 3 pilar
        - Wumpus rör sig mot spelaren 
        """
    )
    difficulty = input().strip().lower()
    while difficulty not in ["1", "2", "3"]:
        print("Fel inmatning, försök igen:")
        difficulty = input().strip().lower()
    
    gameState.difficulty = difficulty

    # Generera noderna
    nodes = generateNodes(difficulty)
    if not nodes:
        print("Kunde inte generera noder.")
        return

    # Hämta spelarens nod
    player = None
    for n in nodes:
        if n.item and n.item.entityType == "P":
            player = n
            break

    # Hämta wumpus nod
    wumpus = None
    for n in nodes:
        if n.item and n.item.entityType == "W":
            wumpus = n
            break

    print("Vill du läsa instruktionerna för hur man spelar? J/N")
    decision = input().strip().lower()
    if decision == "j":
        gameInstructions()
    
    startGame(nodes, player, wumpus)

if __name__ == "__main__":
    main()