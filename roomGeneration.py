import random
from classes import * 
from globalVariables import *
from nodeFunctions import *

#genererar alla rum och ger slumpmässiga väger mellan dem
def generateNodes(difficulty):
    #skapar en lista med alla noder utan något innehåll
    nodes = [Node(i + 1, None, None, None, None, None) for i in range(NODE_COUNT)]
    for node in nodes:
        for direction in ["w", "n", "e", "s"]: #för varje håll i noden
            if getattr(node, direction) == None: #om hållet inte har en nod kopplad
                availableNodes = []
                
                #gå igenom alla noder, lägg till noder som har lediga håll.
                for nd in nodes:
                    if node.id != nd.id: #hitta en nod som inte är sig själv
                        freeDirs = [dirs for dirs in ["w", "n", "e", "s"] if getattr(nd, dirs) is None] #hitta håll som är lediga
                        if freeDirs:
                            availableNodes.append(nd) #om det finns lediga håll, lägg till noden i listan

                #om det finns noder som inte har fått ett håll
                if availableNodes:
                    connectionNode = random.choice(availableNodes) #ta en slumpmässig nod från listan av lediga noder
                    freeDirsForNode = [d for d in ["w", "n", "e", "s"] if getattr(node, d) is None] #hitta lediga noder till den ursprungliga noden

                    if freeDirsForNode: #om det finns lediga håll för noden
                        nodeDir = random.choice(freeDirsForNode) 
                        freeDirsForConnection = [d for d in ["w", "n", "e", "s"] if getattr(connectionNode, d) is None]
                        
                        if freeDirsForConnection:
                            connectionDir = random.choice(freeDirsForConnection) #ta ett slumpmässigt ledigt håll från den slumpmässigt tagna noden
                            #sätt värderna
                            setattr(node, nodeDir, connectionNode.id) 
                            setattr(connectionNode, connectionDir, node.id)

    #efter alla noder har fått ett håll                        
    placeNodeItems(nodes, difficulty)
    return nodes

#placerar spelobjekt i noderna
def placeNodeItems(nodes, difficulty):
    randomItem = lambda outcomes, prob: random.choices(outcomes, weights=prob, k=1) #retunerar ett element ur en lista av element med definerade sannolikheter
    outcomes = [["B", "Jag hör fladdermöss!"], ["H", "Jag känner vinddrag!"], ["N", ""]]
    
    #olika sannolikheter för olika svårighetsgrader
    if difficulty == "1":
        prob = [0.1, 0.05, 0.85]
    elif difficulty == "2":
        prob = [0.2, 0.1, 0.7]
    elif difficulty == "3":
        prob = [0.25, 0.15, 0.6]
    else:
        prob = [0.1, 0.05, 0.85]
    
    #placera spelaren och wumpus först på en slumpmässig plats
    #spelaren placeras
    playerPos = random.randrange(0, NODE_COUNT)
    nodes[playerPos].item = Entity(nodes[playerPos].id, "P")
    #wumpus placeras
    wumpusPos = random.randrange(0, NODE_COUNT)
    while wumpusPos == playerPos: #se till att wumpus inte får samma plats som spelaren
        wumpusPos = random.randrange(0, NODE_COUNT)
    nodes[wumpusPos].item = Entity(nodes[wumpusPos].id, "W", "Du känner lukten av wumpus!") 

    #placera återstående objekt
    for node in nodes:
        if node.item is None:
            item = randomItem(outcomes, prob)
            node.item = Entity(node.id, item[0][0], item[0][1])