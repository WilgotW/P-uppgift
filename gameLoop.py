from classes import *
from globalVariables import *
import os
import random

def getRandomNode(nodes):
    num = random.randrange(0, NODE_COUNT)  
    return nodes[num]

def getNodeItem(nodes, id):
    node = next((n for n in nodes if n.id == id), None)
    return node.item if node else None

def getNode(nodes, id):
    node = next((n for n in nodes if n.id == id), None)
    return node if node else None

def startMessages():
    print("Wumpus")

def startGame(nodes, player, wumpus):
    startMessages()
    playerAction(nodes, player)

def printItemMessage(item):
    match str(item):
        case "W":
            print("Jag känner lukten av Wumpus!")
        case "B":
            print("Jag hör fladdermöss!")
        case "H":
            print("Jag känner vinddrag!")

def printMap(nodes):
    print("\n\n")
    for i in range(len(nodes)):
        if i % 4 == 0:
            print()
        print(nodes[i].item, end="   ")
    
    print("\n\n")
    input()

def playerAction(nodes, player):
    while not gameState.gameOver:
        printMap(nodes)

        checkSurroundingNodes(nodes, player)
        print(f"Du befinner dig i rum: {player.id}")

        print("Härifrån kan man komma till rum: ", end="")
        for dir in ["n", "e", "s", "w"]:
            nodeId = getattr(player, dir)
            print(nodeId, end=", ")
        print("\n\nVad vill du göra:")
        print("1. Rör dig")
        print("2. Skjut")
        print("3. debug")
        print("4. Avsluta \n")
        decision = input()

        while decision not in ["1", "2", "3", "4"]:
            print("Fel inmatning")
            print("1. Rör dig")
            print("2. Skjut")
            decision = input()

        if decision == "1":
            player = playerMove(nodes, player)  
        elif decision == "3":
            print(f"__rum: {player.w}")
        elif decision == "4":
            gameState.gameOver = True

def playerMove(nodes, player):
    directions = ["n", "e", "s", "w"]
    print("Vilket håll? n/e/s/w")
    direction = input().strip().lower()

    while direction not in directions:
        print("Fel inmatning")
        print("Vilket håll? n/e/s/w")
        direction = input().strip().lower()
    
    targetNodeId = getattr(player, direction)
    collisionItem = getNodeItem(nodes, targetNodeId)

    if collisionItem.entityType == "N":
        currentNode = getNode(nodes, player.id)
        currentNode.item = Entity(currentNode.id, "N")
        
        newPlayerNode = getNode(nodes, targetNodeId)
        newPlayerNode.item = Entity(newPlayerNode.id, "P")
        print(f"Du gick in i rum: {newPlayerNode.id}")
        input("...")
        return newPlayerNode
    else:
        return collisionEvent(nodes, collisionItem.entityType, player)

                
def collisionEvent(nodes, collisionType, player):
    if not collisionType == "N": 
        print(f"Du gick in i: {collisionType}")
        input()
    
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
            #remove player from current room
            currentNode = getNode(nodes, player.id)
            currentNode.item = Entity(currentNode.id, "N")
            
            #new room for player
            newNode = getRandomNode(nodes)
            while newNode.item.entityType != "N":
                newNode = getRandomNode(nodes)

            newNode.item = Entity(newNode.id, "P")
            print(f"Du landade i rum: {newNode.id}")
            return newNode

def checkSurroundingNodes(nodes, player):
    for dir in ["n", "e", "s", "w"]:
        nodeId = getattr(player, dir)
        node = getNodeItem(nodes, nodeId)
        if node.entityType != "N":
            print(node.entityMessage)
            
    print()