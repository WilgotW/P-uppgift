import random
from classes import *
from globalVariables import *

def getRandomNodeId(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
    return nodes[num].id

def getNode(nodes, id):
    node = None
    for n in nodes:
        if n.id == id:
            node = n
            break
    return node if node else None

def generateNodes(difficulty):
    # Create nodes with ids 1 through NODE_COUNT, each with no connections.
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]
    
    # For each node, for each direction, if that direction is not yet connected:
    for node in nodes:
        for direction in ["w", "n", "e", "s"]:
            # Only set a connection if this direction is empty.
            if getattr(node, direction) is None:
                # Build a list of candidate nodes that are not the current node.
                candidateNodes = [n for n in nodes if n.id != node.id]
                # Shuffle the candidate list for randomness.
                random.shuffle(candidateNodes)
                connectionNode = None
                connectionDirection = None
                
                # Find the first candidate that has at least one available direction.
                for candidate in candidateNodes:
                    # Get a list of free directions in this candidate node.
                    freeDirections = [d for d in ["w", "n", "e", "s"] if getattr(candidate, d) is None]
                    if freeDirections:
                        connectionNode = candidate
                        connectionDirection = random.choice(freeDirections)
                        break  # Use the first candidate found.
                
                # Only make a connection if a candidate was found.
                if connectionNode:
                    # Set the current node's direction to the candidate's id.
                    setattr(node, direction, connectionNode.id)
                    # Set the candidate node's chosen direction back to the current node's id.
                    setattr(connectionNode, connectionDirection, node.id)
                else:
                    # If no candidate is found, you might log an error or handle it as needed.
                    print(f"Warning: No available node found to connect node {node.id} direction {direction}")
                    
    # Place node items (player, Wumpus, bats, etc.) using the given difficult
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