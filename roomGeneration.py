import random
from classes import *
from globalVariables import *

def getRandomNodeId(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
    return nodes[num].id

def generateNodes(difficulty):
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]

    for node in nodes:
        directions = ["w", "n", "e", "s"]
        for dir in directions:
            nodeId = getRandomNodeId(nodes)
            while nodeId == node.id:
                nodeId = getRandomNodeId(nodes)
            setattr(node, dir, nodeId)

    placeNodeItems(nodes, difficulty)
    return nodes

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)
def placeNodeItems(nodes, difficulty):
    outcomes = [["B",  "Jag hör fladdermöss!"], ["H", "Jag känner vinddrag!"], ["N", ""]] #B = bat. H = hole. N = none
    prob = []#probability of each outcome
    if difficulty == "1":
        prob = [0.1, 0.05, 0.85]
    elif difficulty == "2":
        prob = [0.2, 0.05, 0.75]
    elif difficulty == "3":
        prob = [0.2, 0.1, 0.7]

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