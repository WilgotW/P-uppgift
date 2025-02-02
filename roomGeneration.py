import random
from classes import *
from globalVariables import *

def getRandomNodeId(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
    return nodes[num].id

def generateNodes():
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]

    for node in nodes:
        directions = ["w", "n", "e", "s"]
        for dir in directions:
            nodeId = getRandomNodeId(nodes)
            while nodeId == node.id:
                nodeId = getRandomNodeId(nodes)
            setattr(node, dir, nodeId)

    placeNodeItems(nodes)
    return nodes

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)
def placeNodeItems(nodes):
    outcomes = [["B",  "Jag hör fladdermöss!"], ["H", "Jag känner vinddrag!"], ["N", ""]] #B = bat. H = hole. N = none
    prob = [0.15, 0.05, 0.8] #probability of each outcome

    #place player and wumpus first
    playerPos = random.randrange(0, NODE_COUNT - 1)
    nodes[playerPos].item = Entity(nodes[playerPos].id, "P")
    
    wumpusPos = random.randrange(0, NODE_COUNT - 1)
    while wumpusPos == playerPos:
        wumpusPos = random.randrange(0, NODE_COUNT - 1)
    nodes[wumpusPos].item = Entity(nodes[wumpusPos].id, "W", "Du känner lukten av wumpus!")

    # place remaining items:
    for node in nodes:
        if node.item == None: 
            item = randomItem(outcomes, prob)
            node.item = Entity(node.id, item[0][0], item[0][1]) 