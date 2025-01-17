from classes import * 
from roomGeneration import * 
def main():
    nodes:Node = generateNodes()
    for node in nodes:
        print(node)

main()