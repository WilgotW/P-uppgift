import random
from classes import *
from globalVariables import *
from nodeFunctions import *

def generateNodes(difficulty):
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]
    
    for node in nodes:
        for direction in ["w", "n", "e", "s"]:
            if getattr(node, direction) is None:
                candidateNodes = [n for n in nodes if n.id != node.id]
                random.shuffle(candidateNodes)
                connectionNode = None
                connectionDirection = None
                
                for candidate in candidateNodes:
                    freeDirections = [d for d in ["w", "n", "e", "s"] if getattr(candidate, d) is None]
                    if freeDirections:
                        connectionNode = candidate
                        connectionDirection = random.choice(freeDirections)
                        break 
                
                if connectionNode:
                    setattr(node, direction, connectionNode.id)
                    setattr(connectionNode, connectionDirection, node.id)
                else:
                    print(f"Warning: No available node found to connect node {node.id} direction {direction}")
                    
    placeNodeItems(nodes, difficulty)
    return nodes

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)
def placeNodeItems(nodes, difficulty):
    outcomes = [["B",  "Jag hör fladdermöss!"], ["H", "Jag känner vinddrag!"], ["N", ""]] #B = bat. H = hole. N = none
    prob = []#probability of each outcome
    if difficulty == "1":
        prob = [0.1, 0.05, 0.85]
    elif difficulty == "2":
        prob = [0.2, 0.1, 0.7]
    elif difficulty == "3":
        prob = [0.25, 0.15, 0.6]

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