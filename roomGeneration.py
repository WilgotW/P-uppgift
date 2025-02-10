import random
from classes import * 
from globalVariables import *
from nodeFunctions import *

def generateNodes(difficulty):
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]
    for node in nodes:
        for direction in ["w", "n", "e", "s"]:
            if getattr(node, direction) is None:
                availableNodes = []
                for nd in nodes:
                    if node.id != nd.id:
                        freeDirs = [d for d in ["w", "n", "e", "s"] if getattr(nd, d) is None]
                        if freeDirs:
                            availableNodes.append(nd)
                if availableNodes:
                    connectionNode = random.choice(availableNodes)
                    freeDirsForNode = [d for d in ["w", "n", "e", "s"] if getattr(node, d) is None]
                    if freeDirsForNode:
                        nodeDir = random.choice(freeDirsForNode)
                        freeDirsForConnection = [d for d in ["w", "n", "e", "s"] if getattr(connectionNode, d) is None]
                        if freeDirsForConnection:
                            connectionDir = random.choice(freeDirsForConnection)
                            setattr(node, nodeDir, connectionNode.id)
                            setattr(connectionNode, connectionDir, node.id)
    placeNodeItems(nodes, difficulty)
    return nodes

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)

def placeNodeItems(nodes, difficulty):
    outcomes = [["B", "Jag hör fladdermöss!"], ["H", "Jag känner vinddrag!"], ["N", ""]]
    if difficulty == "1":
        prob = [0.1, 0.05, 0.85]
    elif difficulty == "2":
        prob = [0.2, 0.1, 0.7]
    elif difficulty == "3":
        prob = [0.25, 0.15, 0.6]
    else:
        prob = [0.1, 0.05, 0.85]
    playerPos = random.randrange(0, NODE_COUNT)
    nodes[playerPos].item = Entity(nodes[playerPos].id, "P")
    wumpusPos = random.randrange(0, NODE_COUNT)
    while wumpusPos == playerPos:
        wumpusPos = random.randrange(0, NODE_COUNT)
    nodes[wumpusPos].item = Entity(nodes[wumpusPos].id, "W", "Du känner lukten av wumpus!")
    for node in nodes:
        if node.item is None:
            item = randomItem(outcomes, prob)
            node.item = Entity(node.id, item[0][0], item[0][1])