from classes import *
from globalVariables import *
from textFunctions import *
from nodeFunctions import *
from gui import *

def startGame(nodes, player, wumpus):
    #globala variabler
    arrowsLeft = 3 if gameState.difficulty == "3" else 5
    moves = 0
    
    print("Använd gui? j/n")
    #fel hantering
    guiChoice = input().strip().lower()
    while guiChoice not in ["j", "n"]:
        print("Fel inmatning, prova igen:")
        guiChoice = input().strip().lower()

    if guiChoice == "j":
        startGameGui(nodes, player, wumpus) #kör programmet i gui läget, denna kod fil ignoreras
        return
    else:
        while not gameState.gameOver: #spel loop i konsol läge
            arrowsLeft, moves, player = playerAction(nodes, player, wumpus, arrowsLeft, moves)#updaterar globala variabler och kör programmet
            if gameState.difficulty == "3" and not gameState.gameOver: #wumpus rör sig mot spelaren om svåroghets grad är inställd på svår
                print("Du hör Wumpus röra sig i kulverterna...")
                wumpus = wumpusAI(nodes, wumpus, player, moves) #kör wumpus ai och updatera wumpus Entity

def endGame(won, moves=1):
    gameState.gameOver = True
    if won: #spara resultat i textfil
        with open("highscore.txt", "r+") as file: #"r+": read and write mode. detta gör att vi kan både läsa och skriva i filen
            highscore = file.read()
            if int(highscore) > moves: #kolla om spelaren slog sitt rekord
                print(f"Du slog ditt förra highscore: {highscore}, nytt highscore: {moves}")
                #overwrite förra rekord:
                file.seek(0) #gå till början av filen
                file.write(str(moves)) #skriv nytt rekord, eftersom seek(0) var aktiverat så kommer det förra rekordet att skrivas över
                file.truncate() #radera alla karaktärer efter den nya siffran. funkar bara när det förra rekordet hade fler antal siffor
                #detta görs för att både läsa filen och kunna skriva i den
    else:
        print(f"Du förlorade efter: {moves} drag")

      
def noArrowsLeft(arrowsLeft, moves): #kolla om spelaren har slut på pilar, såfall avsluta spelet
    if arrowsLeft < 1:
        print("Du fick slut på pilar...")
        print("Du förlorade")
        input()
        endGame(True, moves)
        return True
    return False

def playerAction(nodes, player, wumpus, arrowsLeft, moves):
    if noArrowsLeft(arrowsLeft, moves):
        return arrowsLeft, moves, player 
        
    checkSurroundingNodes(nodes, player)#skriv ut objekt i närheten
    printAvaiableDirectios(player) #skriv ut alla håll spelaren kan röra sig

    decision = printMenuOptions(arrowsLeft) #skriv ut meny och ta input
    while decision == "3": #kolla kartan räknas inte som ett drag
        printMap(nodes)
        decision = printMenuOptions(arrowsLeft) #skriv ut meny och ta input

    match decision:
        case "1":
            moves += 1
            player = playerMove(nodes, player, moves)
        case "2":
            moves += 1
            arrowsLeft -= 1
            player = playerShoot(nodes, player, moves)
        case "4":
            endGame(False, moves)
    return arrowsLeft, moves, player

def playerMove(nodes, player, moves):
    directions = ["n", "e", "s", "w"]
    print("Vilket håll? (n/e/s/w)")
    direction = input().strip().lower()
    #fel hantering
    while direction not in directions:
        print("Fel inmatning, försök igen (n/e/s/w):")
        direction = input().strip().lower()
    
    targetNodeId = getattr(player, direction) #det önskade hållet
    collisionItem = getNodeItem(nodes, targetNodeId) #objektet i det önskade hållet

    if collisionItem.entityType == "N": #ifall ingen fanns i det önskade hållet
        currentNode = getNode(nodes, player.id)#nuvarande nod
        currentNode.item = Entity(currentNode.id, "N") #ta bort spelarens position från den nuvarande noden
        
        newPlayerNode = getNode(nodes, targetNodeId)#nya noden
        newPlayerNode.item = Entity(newPlayerNode.id, "P") #sätt spelaren på den nya noden

        print(f"Du gick in i rum: {newPlayerNode.id}")
        return newPlayerNode
    else:
        return collisionEvent(nodes, collisionItem.entityType, player, moves) #ifall det fanns ett objekt i önskade hållet

def collisionEvent(nodes, collisionType, player, moves):
    input("...")
    match collisionType: #olika fall för kollision med spelaren
        case "W":
            print("Du blev uppäten av Wumpus...")
            endGame(False, moves)
            return player
        case "H":
            print("Du föll ner i ett bottenlöst hål...")
            endGame(False, moves)
            return player
        case "B":
            print("Du känner fladdermusvingar mot kinden och lyfts uppåt")

            currentNode = getNode(nodes, player.id)
            currentNode.item = Entity(currentNode.id, "N") #ta bort spelaren från nuvarande nod
            
            newNode = getRandomNode(nodes) #hämta en slumpmässig nod
            while newNode.item.entityType != "N": #gör om tills en tom nod hittas
                newNode = getRandomNode(nodes)

            newNode.item = Entity(newNode.id, "P") #sätt spelaren på nya slumpmässiga noden
            print(f"Du landade i rum: {newNode.id}")
            return newNode
    input("...")
    return player  

def playerShoot(nodes, player, moves):
    print("Du har valt att skjuta en pil.")
    arrowRoomId = player.id #initiera pilen på spelarens nod
    amount = 3 #antal rum pilen färdas genom

    for i in range(amount):
        print(f"Rum {i+1} av {amount}: Pilen befinner sig i rum {arrowRoomId}.")
        direction = printArrowDirections() #spelaren inmatar nytt håll för pilen

        currentArrowNode = getNode(nodes, arrowRoomId) #nuvarande nod
        arrowRoomId = getattr(currentArrowNode, direction) #nya nodens id

        print(f"Pilen flyttas till rum: {arrowRoomId}")

        roomItem = getNodeItem(nodes, arrowRoomId) #hämta nya rummets objekt
        if roomItem.entityType == "W": #kolla ifall objektet är wumpus
            print("Du träffade Wumpus med pilen! Du vann!")
            endGame(True, moves)
            return player 

    print("Pilen nådde sin maximala räckvidd och missade Wumpus.")
    input("...")
    return player

def checkSurroundingNodes(nodes, player): #skriv ut alla varningsmeddelande av objekt i närheten om spelaren
    messages = []
    for direction in ["n", "e", "s", "w"]: 
        nodeId = getattr(player, direction)
        nodeItem = getNodeItem(nodes, nodeId)
        #lägg till alla meddelande i listan messages
        if nodeItem is not None and nodeItem.entityType != "N": 
            messages.append(nodeItem.entityMessage)
        
    messageCounts = {} #spara antalet för dubbletter
    for msg in messages:
        if msg in messageCounts: #om meddelandet redan finns, öka antalet
            messageCounts[msg] += 1
        else:
            messageCounts[msg] = 1
    for msg, count in messageCounts.items(): #skriv ut alla varningsmeddelande och antal
        if count > 1:
            print(f"{msg} x{count}")
        else:
            print(msg)


#flyttar wumpus mot spelaren med kortaste vägen
def wumpusAI(nodes, wumpusNode, playerNode, moves):
    #om wumpus eller spelaren saknas, returnera nuvarande wumpusnod
    if wumpusNode is None or playerNode is None:
        return wumpusNode
    #hitta kortaste vägen från wumpus till spelaren
    path = bfsPath(nodes, wumpusNode.id, playerNode.id)
    #om en giltig väg hittas och den innehåller mer än ett steg
    if path and len(path) > 1:
        #väljer nästa nod längs vägen
        nextId = path[1]
        #hämtar nuvarande nod och tar bort wumpus från den
        oldNode = getNode(nodes, wumpusNode.id)
        oldNode.item = Entity(oldNode.id, "N")
        #om nästa nod är spelarens nod, wumpus når spelaren
        if nextId == playerNode.id:
            print("wumpus rörde sig in i ditt rum!")
            endGame(False, moves)
            return wumpusNode
        #flyttar wumpus till nästa nod
        newWumpusNode = getNode(nodes, nextId)
        newWumpusNode.item = Entity(newWumpusNode.id, "W", "du känner lukten av wumpus!")
        return newWumpusNode
    return wumpusNode

#hittar kortaste vägen mellan två noder
def bfsPath(nodes, startId, goalId): #breadth first search
    #initierar kö med startnod, markerar den som besökt och sätter dess förälder till None
    queue = [startId]
    visited = {startId}
    parent = {startId: None}

    #loopar tills kön är tom
    while queue:
        current = queue.pop(0)
        #om målnoden hittas, bygg upp vägen genom att följa föräldrar
        if current == goalId:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        #hämtar nuvarande nod
        currentNode = getNode(nodes, current)
        #går igenom alla fyra riktningar
        for d in ["n", "e", "s", "w"]:
            neighborId = getattr(currentNode, d)
            #om grannnoden finns och inte besökt, lägg till den
            if neighborId is not None and neighborId not in visited:
                visited.add(neighborId)
                parent[neighborId] = current
                queue.append(neighborId)

    #om ingen väg hittas, returnera None
    return None

