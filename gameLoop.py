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
    gui_choice = input().strip().lower()
    while gui_choice not in ["j", "n"]:
        print("Fel inmatning, prova igen:")
        gui_choice = input().strip().lower()

    if gui_choice == "j":
        # Run the GUI game loop (the new, event-driven version)
        startGameGui(nodes, player, wumpus)
        return
    else:
        while not gameState.gameOver:
            arrowsLeft, moves, player = playerAction(nodes, player, wumpus, arrowsLeft, moves)

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
      
def noArrowsLeft(arrowsLeft, moves):
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
    checkSurroundingNodes(nodes, player)
    printAvaiableDirectios(player)

    decision = printMenuOptions(arrowsLeft) #skriv ut meny och ta input
    match decision:
        case "1":
            moves += 1
            player = playerMove(nodes, player, moves)
        case "2":
            moves += 1
            arrowsLeft -= 1
            player = playerShoot(nodes, player, moves)
        case "3":
            printMap(nodes)
        case "4":
            endGame(False, moves)  
    return arrowsLeft, moves, player

def playerMove(nodes, player, moves):
    directions = ["n", "e", "s", "w"]
    print("Vilket håll? (n/e/s/w)")
    direction = input().strip().lower()

    while direction not in directions:
        print("Fel inmatning, försök igen (n/e/s/w):")
        direction = input().strip().lower()
    
    targetNodeId = getattr(player, direction) #det önskade hållet
    collisionItem = getNodeItem(nodes, targetNodeId) #objektet i den önskade hållet

    if collisionItem.entityType == "N": #ifall ingen fanns i det önskade hållet
        currentNode = getNode(nodes, player.id)
        currentNode.item = Entity(currentNode.id, "N") #ta bort spelarens position från den nuvarande noden
        
        newPlayerNode = getNode(nodes, targetNodeId)
        newPlayerNode.item = Entity(newPlayerNode.id, "P") #sätt spelaren på den nya noden

        print(f"Du gick in i rum: {newPlayerNode.id}")
        return newPlayerNode
    else:
        return collisionEvent(nodes, collisionItem.entityType, player, moves) #ifall det fanns ett objekt i önskade hållet

def collisionEvent(nodes, collisionType, player, moves):
    input("...")
    match collisionType:
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
    steps = 3 #antal rum pilen färdas i

    for i in range(steps):
        print(f"Rum {i+1} av {steps}: Pilen befinner sig i rum {arrowRoomId}.")
        direction = printArrowDirections()

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
        if nodeItem.entityType != "N": #gå igenom alla håll och spara objektets varningsmeddelelande ifall det finns ett objekt
            messages.append(nodeItem.entityMessage)
        
    messageCounts = {} #spara antalet för alla meddelande
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