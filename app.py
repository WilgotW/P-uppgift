from classes import * 
from roomGeneration import * 
from gameLoop import * 

def main():
    nodes = generateNodes()
    for n in nodes:
        print(f"Node ID: {n.id}, Item: {n.item.__dict__ if n.item else 'None'}")

    # Get the player and wumpus 
    player = next((n for n in nodes if n.item and n.item.entityType == "P"), None)
    wumpus = next((n for n in nodes if n.item and n.item.entityType == "W"), None)   

    startGame(nodes, player, wumpus)

main()