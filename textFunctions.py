import os

def printMenuOptions(arrowsLeft):
    print("\n\n")
    #os.system('clear')

    print("\nVad vill du göra:")
    print("1. Rör dig")
    print(f"2. Skjut pil ({arrowsLeft})")
    print("3. Kolla på kartan")
    print("4. Avsluta")
    decision = input().strip()

    while decision not in ["1", "2", "3", "4"]:
        print("Fel inmatning")
        print("1. Rör dig")
        print(f"2. Skjut pil ({arrowsLeft})")
        print("3. Kolla på kartan")
        print("4. Avsluta")
        decision = input().strip()
    return decision


def printAvaiableDirectios(player):
    print(f"\nDu befinner dig i rum: {player.id}")
    print("Härifrån kan man komma till rum: ", end="")
    for dir in ["n", "e", "s", "w"]:
        nodeId = getattr(player, dir)
        print(nodeId, end=", ")
    print()

def printItemMessage(item):
    match str(item):
        case "W":
            print("Jag känner lukten av Wumpus!")
        case "B":
            print("Jag hör fladdermöss!")
        case "H":  
            print("Jag känner vinddrag!")

def printMap(nodes):
    os.system('clear')
    for i in range(len(nodes)):
        if i % 4 == 0:
            print()
        print(nodes[i].item, end="   ")
    
    print("\n\n")
    input("...")
    os.system("clear")

def printArrowDirections():
    print("I vilken riktning ska pilen flyga? (n/e/s/w)")
    direction = input().strip().lower()
    while direction not in ["n", "e", "s", "w"]:
        print("Fel inmatning, försök igen (n/e/s/w):")
        direction = input().strip().lower()
    return direction 