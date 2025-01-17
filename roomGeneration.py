import random
from classes import *

def generateNodes():
    nodes:Node = []
    for i in range(20):
        newNode = Node(None, None, None, None, None)
        nodes.append(newNode)
    
    for node in nodes:
        node.n = getRandomNodeId(nodes)
        node.e = getRandomNodeId(nodes)
        node.s = getRandomNodeId(nodes)
        node.n = getRandomNodeId(nodes)

    placeNodeItems(nodes)
    return nodes

def getRandomNodeId(nodes):
    num = random.randrange(0, 19)
    return nodes[num].id

randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1)[0]
def placeNodeItems(nodes):
    outcomes = ["B", "H", "N"] #B = bat. H = hole. N = none
    prob = [0.1, 0.05, 0.85] #probability of each outcome

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


