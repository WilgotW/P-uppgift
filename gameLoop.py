from classes import * 
from globalVariables import *
import os

def getRandomNode(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
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

def printMap(nodes:Node):
    print("\n \n")
    # os.system('clear')
    for i in range(len(nodes)):
        if (i) % 4 == 0:
            print()
        print(nodes[i].item, end="   ")
    
    print("\n \n")
    input()

def playerAction(nodes, player):
    while not gameState.gameOver:
        # os.system('clear')
      
        # for n in nodes:
        #     print(f"Node ID: {n.id}, Item: {n.item.__dict__ if n.item else 'None'}")
        printMap(nodes)
        print("Härifrån kan man komma till rum: ", end="")
        directions = ["n", "e", "s", "w"]
        for dir in directions:
            nodeId = getattr(player, dir)
            nodeItem = getNodeItem(nodes, nodeId)
            # print(str(nodes.index(getNode(nodes, getattr(player, dir)))), end=", ")
            print(nodeId, end=", ")

            #printItemMessage(nodeItem)
        print()
        
        print("Vad vill du göra:")
        print("1. Rör dig")
        print("2. Skjut")
        decision = input()

        while decision not in ["1", "2"]:
            print("Fel inmatning")
            print("1. Rör dig")
            print("2. Skjut")
            decision = input()

        if decision == "1":
            player = playerMove(nodes, player)  

def playerMove(nodes, player):
    directions = ["n", "e", "s", "w"]
    print("Vilket håll? n/e/s/w")
    direction = input().strip().lower()

    while direction not in directions:
        print("Fel inmatning")
        print("Vilket håll? n/e/s/w")
        direction = input().strip().lower()
    
    targetNodeId = getattr(player, direction)
    targetNode = getNode(nodes, targetNodeId)

    collisionItem = getNodeItem(nodes, targetNodeId)

    if collisionItem and collisionItem.entityType in ["N", None]: 
        for node in nodes:
            if node.id == player.id:
                node.item = Entity(node.id, "N") 
            if node.id == targetNodeId:
                node.item = Entity(node.id, "P")
                print(f"Du gick in i rum: {node.id}")
        player.id = targetNodeId
        input("...")
        return player
    else:
        player = collisionEvent(nodes, collisionItem.entityType, player)
        return player
    

def collisionEvent(nodes, collisionItem, player):
    print(f"Du gick in i: {collisionItem}")
    input()
    match collisionItem:
        case "W":
            print("Du blev uppäten av Wumpus...")
            gameState.gameOver = True
        case "H":
            print("Du föll ner i ett bottenlöst hål...")
            gameState.gameOver = True
        case "B":
            print("Du känner fladdermusvingar mot kinden och lyfts uppåt")
            for node in nodes:
                if node.id == player.id:
                    node.item = Entity(node.id, "N") 
            node = getRandomNode(nodes)
            while not node.item.entityType == "N":
                node = getRandomNode(nodes)

            node.item = Entity(node.id, "P")
            player.id = node.id
            print(f"du landade i rum: {node.id}")
            return player




