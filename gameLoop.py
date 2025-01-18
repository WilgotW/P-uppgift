from classes import * 

def getNodeItem(nodes:Node, id):
    node = next((n for n in nodes if n.id and n.id == id), None)
    return node.item

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
        case "W":
            print("Jag känner vinddrag!")

def playerAction(nodes, player:Node):
    directions = ["n", "e", "s", "w"]
    for dir in directions:
        nodeItem = getNodeItem(nodes, getattr(player, dir))
        printItemMessage(nodeItem)
    
    print("Vad vill du göra:")
    print("1. Rör dig")
    print("2. Skjut")
    decision = input()

    while not decision == "1" and not decision == "2":
        print("Fel inmatning")
        print("1. Rör dig")
        print("2. Skjut")
        decision = input()

    if decision == 1:
        print()


def playerMove():
    print("Vilket håll?")