from globalVariables import * 
import random

#retunerar en slumpmässig nods ID
def getRandomNodeId(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
    return nodes[num].id

#retunerar en slumpmässig nod index
def getRandomNode(nodes):
    num = random.randrange(0, NODE_COUNT)
    return nodes[num]

#retunera en nods objekt (Entity) från inmatad nod ID
def getNodeItem(nodes, id):
    node = None
    for n in nodes:
        if n.item and n.id == id:
            node = n
            break
    return node.item if node else None

#returnerar nod från inmatad nod ID
def getNode(nodes, id):
    node = None
    for n in nodes:
        if n.id == id:
            node = n
            break
    return node if node else None
