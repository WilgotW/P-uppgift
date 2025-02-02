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


def startGame(nodes, player, wumpus, difficulty):
    while not gameState.gameOver:
        playerAction(nodes, player, wumpus)
        if(difficulty == "Hard"):
            wumpusMove()
        

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

def wumpusMove():
    print("Du hör hur Wumpus rör sig i kulverterna...")

    input("...")

def playerAction(nodes, player, wumpus):
    print("\n\n")

    os.system('clear')

    checkSurroundingNodes(nodes, player)

    print(f"\nDu befinner dig i rum: {player.id}")
    print("Härifrån kan man komma till rum: ", end="")
    for dir in ["n", "e", "s", "w"]:
        nodeId = getattr(player, dir)
        print(nodeId, end=", ")
    print()
    
    print("\nVad vill du göra:")
    print("1. Rör dig")
    print("2. Skjut pil")
    print("3. Kolla på kartan")
    print("4. Avsluta")
    decision = input().strip()

    while decision not in ["1", "2", "3", "4"]:
        print("Fel inmatning")
        print("1. Rör dig")
        print("2. Skjut pil")
        decision = input().strip()

    if decision == "1":
        player = playerMove(nodes, player)
    elif decision == "2":
        player = playerShoot(nodes, player, wumpus)
    elif decision == "3":
        printMap(nodes)
    elif decision == "4":
        gameState.gameOver = True

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
        input("Tryck Enter för att fortsätta...")
        return newPlayerNode
    else:
        return collisionEvent(nodes, collisionItem.entityType, player)
    
def playerShoot(nodes, player, wumpus):
    print("Du har valt att skjuta en pil.")
    arrow_room_id = player.id
    steps = 3

    for i in range(steps):
        print(f"\Rum {i+1} av {steps}: Pilen befinner sig i rum {arrow_room_id}.")
        print("I vilken riktning ska pilen flyga? (n/e/s/w)")
        direction = input().strip().lower()
        while direction not in ["n", "e", "s", "w"]:
            print("Fel inmatning, försök igen (n/e/s/w):")
            direction = input().strip().lower()

        current_arrow_node = getNode(nodes, arrow_room_id)
        arrow_room_id = getattr(current_arrow_node, direction)
        print(f"Pilen flyttas till rum: {arrow_room_id}")

        roomItem = getNodeItem(nodes, arrow_room_id)
        if roomItem.entityType == "W":
            print("Du träffade Wumpus med pilen! Du vann!")
            gameState.gameOver = True
            input("Tryck Enter för att avsluta spelet...")
            return player 

    print("Pilen nådde sin maximala räckvidd och missade Wumpus.")
    input("Tryck Enter för att fortsätta...")
    return player

def collisionEvent(nodes, collisionType, player):
    input("...")
    match collisionType:
        case "W":
            print("Du blev uppäten av Wumpus...")
            gameState.gameOver = True
            return player
        case "H":
            print("Du föll ner i ett bottenlöst hål...")
            gameState.gameOver = True
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
        node = getNodeItem(nodes, nodeId)
        if node.entityType != "N":
            messages.append(node.entityMessage)
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
