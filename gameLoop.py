from classes import * 
import os

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

def playerAction(nodes, player):
    while True:
        os.system('clear')
        # for n in nodes:
        #     print(f"Node ID: {n.id}, Item: {n.item.__dict__ if n.item else 'None'}")

        directions = ["n", "e", "s", "w"]
        for dir in directions:
            nodeItem = getNodeItem(nodes, getattr(player, dir))
            print("rum: " + str(nodes.index(getNode(nodes, getattr(player, dir)))))
            #printItemMessage(nodeItem)
        
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
    
    target_node_id = getattr(player, direction)
    target_node = getNode(nodes, target_node_id)

    collisionItem = getNodeItem(nodes, target_node_id)

    if collisionItem and collisionItem.entityType in ["N", None]: 
        for node in nodes:
            if node.id == player.id:
                node.item = Entity(node.id, "N") 
            if node.id == target_node_id:
                node.item = Entity(node.id, "P")
        player.id = target_node_id
        return player
    else:
        print(f"Du gick in i: {collisionItem.entityType if collisionItem else 'None'}")
        return player