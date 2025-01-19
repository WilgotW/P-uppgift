import random
from classes import *

def getRandomNodeId(nodes):
    num = random.randrange(0, 19)
    return nodes[num].id

def generateNodes():
    nodes = [Node(i, None, None, None, None) for i in range(20)]

    for node in nodes:
        directions = ["w", "n", "e", "s"]
        for dir in directions:
            nodeId = getRandomNodeId(nodes)
            while nodeId == node.id:
                nodeId = getRandomNodeId(nodes)
            setattr(node, dir, nodeId)

    placeNodeItems(nodes)
    return nodes

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)[0]
def placeNodeItems(nodes):
    outcomes = ["B", "H", "N"] #B = bat. H = hole. N = none
    prob = [0.25, 0.15, 0.6] #probability of each outcome

    #place player and wumpus first
    playerPos = random.randrange(0, 19)
    nodes[playerPos].item = Entity(nodes[playerPos].id, "P")
    
    wumpusPos = random.randrange(0, 19)
    while wumpusPos == playerPos:
            wumpusPos = random.randrange(0, 19)
    nodes[wumpusPos].item = Entity(nodes[wumpusPos].id, "W")

    # place remaining items:
    for node in nodes:
        if node.item == None: 
            node.item = Entity(node.id, randomItem(outcomes, prob)[0]) 