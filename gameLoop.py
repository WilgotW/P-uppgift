from classes import *
from globalVariables import *
import os
import random

def getRandomNode(nodes):
    num = random.randrange(0, NODE_COUNT)  # adjusted to use all nodes
    return nodes[num]

def getNodeItem(nodes, id):
    node = next((n for n in nodes if n.id == id), None)
    return node.item if node else None

def getNode(nodes, id):
    node = next((n for n in nodes if n.id == id), None)
    return node if node else None


def startGame(nodes, player, wumpus):
    arrowsLeft = 3 if gameState.difficulty == "3" else 5
    moves = 0
    while not gameState.gameOver:
        arrowsLeft, moves = playerAction(nodes, player, wumpus, arrowsLeft, moves)
        

def printItemMessage(item):
    match str(item):
        case "W":
            print("Jag känner lukten av Wumpus!")
        case "B":
            print("Jag hör fladdermöss!")
        case "H":  
            print("Jag känner vinddrag!")

def printMap(nodes):
    os.system('clear')
    for i in range(len(nodes)):
        if i % 4 == 0:
            print()
        print(nodes[i].item, end="   ")
    
    print("\n\n")
    input("...")
    os.system("clear")

def endGame(won, moves = 1):
    gameState.gameOver = True
    if won:
        with open("highscore.txt", "r+") as file:
            highscore = file.read()
            #spelaren vann, sparar highscore
            if int(highscore) > moves:
                print(f"Du slog ditt förra highscore: {highscore}, nytt highscore: {moves}")
                file.seek(0)
                file.write(str(moves)) 
                file.truncate()
    else:
        print(f"Du förlorade efter: {moves} drag") 
      
def wumpusMove():
    if gameState.gameOver == True: return
    print("\nDu hör hur Wumpus rör sig i kulverterna...")
    input("...")

def playerAction(nodes, player, wumpus, arrowsLeft, moves):
    print("\n\n")
    os.system('clear')

    if arrowsLeft < 1:
        print("Du fick slut på pilar...")
        print("du förlorade")
        input()
        endGame(True, moves)
        return
    
    checkSurroundingNodes(nodes, player)
    print(f"\nDu befinner dig i rum: {player.id}")
    print("Härifrån kan man komma till rum: ", end="")
    for dir in ["n", "e", "s", "w"]:
        nodeId = getattr(player, dir)
        print(nodeId, end=", ")
    print()
    
    print("\nVad vill du göra:")
    print("1. Rör dig")
    print(f"2. Skjut pil ({arrowsLeft})")
    print("3. Kolla på kartan")
    print("4. Avsluta")
    decision = input().strip()

    while decision not in ["1", "2", "3", "4"]:
        print("Fel inmatning")
        print("1. Rör dig")
        print(f"2. Skjut pil ({arrowsLeft})")
        print("3. Kolla på kartan")
        print("4. Avsluta")
        decision = input().strip()

    if decision == "1":
        moves += 1
        player = playerMove(nodes, player)
        if(gameState.difficulty == "3"):
            wumpusMove()
    elif decision == "2":
        moves += 1
        arrowsLeft -= 1
        player = playerShoot(nodes, player, wumpus, moves)
        if(gameState.difficulty == "3"):
            wumpusMove()
        
    elif decision == "3":
        printMap(nodes)
    elif decision == "4":
        endGame(False)
    
    return arrowsLeft, moves

def playerMove(nodes, player):
    directions = ["n", "e", "s", "w"]
    print("Vilket håll? (n/e/s/w)")
    direction = input().strip().lower()

    while direction not in directions:
        print("Fel inmatning, försök igen (n/e/s/w):")
        direction = input().strip().lower()
    
    targetNodeId = getattr(player, direction)
    collisionItem = getNodeItem(nodes, targetNodeId)

    if collisionItem.entityType == "N":
        currentNode = getNode(nodes, player.id)
        currentNode.item = Entity(currentNode.id, "N")
        
        newPlayerNode = getNode(nodes, targetNodeId)
        newPlayerNode.item = Entity(newPlayerNode.id, "P")
        print(f"Du gick in i rum: {newPlayerNode.id}")
        return newPlayerNode
    else:
        return collisionEvent(nodes, collisionItem.entityType, player)
    
def playerShoot(nodes, player, wumpus, moves):
    print("Du har valt att skjuta en pil.")
    arrowRoomId = player.id
    steps = 3

    for i in range(steps):
        print(f"Rum {i+1} av {steps}: Pilen befinner sig i rum {arrowRoomId}.")
        print("I vilken riktning ska pilen flyga? (n/e/s/w)")
        direction = input().strip().lower()
        while direction not in ["n", "e", "s", "w"]:
            print("Fel inmatning, försök igen (n/e/s/w):")
            direction = input().strip().lower()

        current_arrow_node = getNode(nodes, arrowRoomId)
        arrowRoomId = getattr(current_arrow_node, direction)
        print(f"Pilen flyttas till rum: {arrowRoomId}")

        roomItem = getNodeItem(nodes, arrowRoomId)
        if roomItem.entityType == "W":
            print("Du träffade Wumpus med pilen! Du vann!")
            endGame(True, moves)
            return player 

    print("Pilen nådde sin maximala räckvidd och missade Wumpus.")
    input("Tryck Enter för att fortsätta...")
    return player

def collisionEvent(nodes, collisionType, player):
    input("...")
    match collisionType:
        case "W":
            print("Du blev uppäten av Wumpus...")
            endGame(False)
            return player
        case "H":
            print("Du föll ner i ett bottenlöst hål...")
            endGame(False)
            return player
        case "B":
            print("Du känner fladdermusvingar mot kinden och lyfts uppåt")
            currentNode = getNode(nodes, player.id)
            currentNode.item = Entity(currentNode.id, "N")
            
            newNode = getRandomNode(nodes)
            while newNode.item.entityType != "N":
                newNode = getRandomNode(nodes)

            newNode.item = Entity(newNode.id, "P")
            print(f"Du landade i rum: {newNode.id}")
            return newNode
    input("...")

def checkSurroundingNodes(nodes, player):
    messages = []
    for direction in ["n", "e", "s", "w"]:
        nodeId = getattr(player, direction)
        nodeItem = getNodeItem(nodes, nodeId)
        if nodeItem.entityType != "N":
            messages.append(nodeItem.entityMessage)
    messageCounts = {}
    for msg in messages:
        if msg in messageCounts:
            messageCounts[msg] += 1
        else:
            messageCounts[msg] = 1
    for msg, count in messageCounts.items():
        if count > 1:
            print(f"{msg} x{count}")
        else:
            print(msg)
