from globalVariables import * 

def getRandomNodeId(nodes):
    num = random.randrange(0, NODE_COUNT - 1)
    return nodes[num].id

def getRandomNode(nodes):
    num = random.randrange(0, NODE_COUNT)
    return nodes[num]

def getNodeItem(nodes, id):
    node = None
    for n in nodes:
        if n.item and n.id == id:
            node = n
            break
    return node.item if node else None

def getNode(nodes, id):
    node = None
    for n in nodes:
        if n.id == id:
            node = n
            break
    return node if node else None
