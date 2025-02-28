from classes import *
from globalVariables import *
from nodeFunctions import *
from textFunctions import *
import tkinter as tk
from tkinter import messagebox

def guiLoop(player):
    #skapa fönster
    root = tk.Tk()
    root.title("Wumpus")
    root.geometry("500x400")

    #skapa textruta som visar spelarens rum
    label = tk.Label(root, text=f"du befinner dig i rum: {player.id}", font=("Arial", 16))
    label.pack(pady=20)

    #uppdaterar textrutan vid händelse 
    def updateLabel():
        label.config(text=f"du befinner dig i rum: {player.id}")
        root.update_idletasks()
    updateLabel()
    
    #startar loop
    root.mainloop()

def startGameGui(nodes, player, wumpus):
    arrowsLeft = 3 if gameState.difficulty == "3" else 5
    moves = 0

    #huvudsakligt fönster för spelet
    root = tk.Tk()
    root.title("Wumpus GUI")
    root.geometry("600x400")
    
    #textfält för spelmeddelanden
    messageText = tk.Text(root, height=10, width=70)
    messageText.pack(pady=10)
    #textruta för spelarens rum
    roomLabel = tk.Label(root, text=f"du befinner dig i rum: {player.id}", font=("Arial", 16))
    roomLabel.pack(pady=5)
    
    #ram för menyknappar
    buttonFrame = tk.Frame(root)
    buttonFrame.pack(pady=10)

    #knappar för menyn
    moveButton = tk.Button(buttonFrame, text="rör dig", width=10, command=lambda: moveAction())
    shootButton = tk.Button(buttonFrame, text=f"skjut ({arrowsLeft})", width=10, command=lambda: playerShoot())
    mapButton = tk.Button(buttonFrame, text="kolla kartan", width=10, command=lambda: viewMap())
    quitButton = tk.Button(buttonFrame, text="avsluta", width=10, command=lambda: quitGame())
   
    #placerar knapparna i ett rutnät
    moveButton.grid(row=0, column=0, padx=5)
    shootButton.grid(row=0, column=1, padx=5)
    mapButton.grid(row=0, column=2, padx=5)
    quitButton.grid(row=0, column=3, padx=5)
    
    #alla spelets variabler sparas i state
    state = {
        "arrowsLeft": arrowsLeft,
        "moves": moves,
        "player": player,
        "nodes": nodes,
        "wumpus": wumpus,
        "gameOver": False,
    }

    #lägger till ett meddelande i textfältet
    def appendMessage(msg):
        messageText.insert(tk.END, msg + "\n")
        messageText.see(tk.END)

    #uppdaterar textfältet som visar spelarens aktuella rum
    def updateRoomLabel():
        roomLabel.config(text=f"Du befinner dig i rum: {state['player'].id}")

    #inaktivera alla knappar om spelet är över
    def checkGameOver():
        if state["gameOver"]:
            moveButton.config(state=tk.DISABLED)
            shootButton.config(state=tk.DISABLED)
            mapButton.config(state=tk.DISABLED)
            quitButton.config(state=tk.DISABLED)

    #kolla noder och skriver ut varningsmeddelanden
    def checkSurroundingNodes():
        messages = []
        for direction in ["n", "e", "s", "w"]:
            nodeId = getattr(state["player"], direction)
            nodeItem = getNodeItem(state["nodes"], nodeId)

            #om noden innehåller ett objekt, lägg till meddelandet
            if nodeItem is not None and nodeItem.entityType != "N":
                messages.append(nodeItem.entityMessage)
        
        messageCounts = {}
        #räknar antalet av dubbletter.
        for msg in messages:
            if msg in messageCounts:
                messageCounts[msg] += 1
            else:
                messageCounts[msg] = 1
        #skriver ut meddelandena med antal av dubbletter
        for msg, count in messageCounts.items():
            if count > 1:
                appendMessage(f"{msg} x{count}")
            else:
                appendMessage(msg)

    #be om riktning
    def moveAction():
        askDirection("rör dig", "välj riktning att gå:", processMoveDirection)

    #tar spelarens valda riktning och flyttar spelaren
    def processMoveDirection(direction):
        state["moves"] += 1
        targetNodeId = getattr(state["player"], direction)

        if targetNodeId is None:
            appendMessage("det finns ingen dörr i den riktningen!")
            return
        collisionItem = getNodeItem(state["nodes"], targetNodeId)

        if collisionItem is None:
            appendMessage("rummet i den riktningen existerar inte!")
            return
        
        if collisionItem.entityType == "N":
            #ta bort spelaren från nuvarande nod
            currentNode = getNode(state["nodes"], state["player"].id)
            currentNode.item = Entity(currentNode.id, "N")
            #sätt spelaren på den nya noden
            newPlayerNode = getNode(state["nodes"], targetNodeId)
            newPlayerNode.item = Entity(newPlayerNode.id, "P")
            state["player"] = newPlayerNode

            appendMessage(f"du gick in i rum: {newPlayerNode.id}.")
            updateRoomLabel()
            checkSurroundingNodes()
        else:
            
            collisionEvent(collisionItem.entityType)#kollision 
        checkGameOver()

    #hanterar kollision med objekt
    def collisionEvent(collisionType):
        if collisionType == "W":
            appendMessage("du blev uppäten av wumpus...")
            endGame(False)

        elif collisionType == "H":
            appendMessage("du föll ner i ett bottenlöst hål...")
            endGame(False)

        elif collisionType == "B":
            appendMessage("fladdermöss lyfter upp dig!")
            #tar bort spelaren från nuvarande nod
            currentNode = getNode(state["nodes"], state["player"].id)
            currentNode.item = Entity(currentNode.id, "N")

            newNode = getRandomNode(state["nodes"])

            #letar efter en tom nod att placera spelaren i
            while getNodeItem(state["nodes"], newNode.id).entityType != "N":
                newNode = getRandomNode(state["nodes"])

            newNode.item = Entity(newNode.id, "P")
            state["player"] = newNode

            appendMessage(f"du landade i rum: {newNode.id}.")
            updateRoomLabel()
            checkSurroundingNodes()

    #hanterar pil skjutning
    def playerShoot():
        if state["arrowsLeft"] < 1:
            appendMessage("du fick slut på pilar! du förlorade!")
            endGame(False)
            return
        
        state["arrowsLeft"] -= 1
        state["moves"] += 1
        arrowRoomId = state["player"].id

        shootArrowStep(1, arrowRoomId)

    #flyttar pilen stegvis genom noderna
    def shootArrowStep(step, arrowRoomId):
        if step > 3:
            appendMessage("pilen missade wumpus.")
            return
        
        appendMessage(f"pilen befinner sig i rum {arrowRoomId} (steg {step}).")
        askDirection("skjut", "välj riktning för pilen:", lambda d: processShootStep(step, arrowRoomId, d))

    #pilens rörelse, kontrollerar om pilen träffar wumpus
    def processShootStep(step, arrowRoomId, direction):
        currentArrowNode = getNode(state["nodes"], arrowRoomId)
        newArrowRoomId = getattr(currentArrowNode, direction)

        appendMessage(f"pilen flyttas till rum: {newArrowRoomId}.")
        roomItem = getNodeItem(state["nodes"], newArrowRoomId)

        if roomItem.entityType == "W":
            appendMessage("du träffade wumpus med pilen!")
            endGame(True)
            return
        else:
            shootArrowStep(step + 1, newArrowRoomId)

    #visar hela nod listan och alla objekt
    def viewMap():
        mapWin = tk.Toplevel(root)
        mapWin.title("karta")
        text = tk.Text(mapWin, height=10, width=50)
        text.pack()
        cols = 4
        #loopen går igenom varje nod med enumerate, detta ger både index och värdet för varje element
        for i, node in enumerate(state["nodes"]):
            text.insert(tk.END, f"{node.item.entityType} ")
            #ser till att texten blir uppdelad i kolumner och rader
            if (i+1) % cols == 0:
                text.insert(tk.END, "\n")
        #textfältet icke redigerbart
        text.config(state=tk.DISABLED)

    #avsluta spelet
    def quitGame():
        appendMessage("spelet är över. du avslutade.")
        endGame(False)

    #avslutar spelet, uppdaterar highscore och visar ett meddelande
    def endGame(won):
        state["gameOver"] = True
        if won:
            recordMessage = ""
            with open("highscore.txt", "r+") as file:
                content = file.read().strip()
                if content:
                    highscore = int(content)
                else:
                    highscore = None
                if highscore is None or state["moves"] < highscore:
                    if highscore is not None:
                        recordMessage = f"du slog ditt tidigare rekord på {highscore} drag!"
                    else:
                        recordMessage = "detta är ditt första rekord!"
                    file.seek(0)
                    file.write(str(state["moves"]))
                    file.truncate()
                else:
                    recordMessage = f"ditt bästa rekord är {highscore} drag."

        else:
            msg = f"spelet är över! du förlorade efter {state['moves']} drag."
        appendMessage(msg)
        checkGameOver()
        messagebox.showinfo("spelet är över", msg)
        root.destroy()

    #öppnar en dialogruta för att fråga användaren om en riktning
    def askDirection(title, prompt, callback):
        win = tk.Toplevel(root)
        win.title(title)
        tk.Label(win, text=prompt).pack(pady=10)

        btnFrame = tk.Frame(win)
        btnFrame.pack(pady=5)

        def select(direction):
            callback(direction)
            win.destroy()
            
        tk.Button(btnFrame, text="norr", width=10, command=lambda: select("n")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btnFrame, text="väst", width=10, command=lambda: select("w")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btnFrame, text="öster", width=10, command=lambda: select("e")).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(btnFrame, text="söder", width=10, command=lambda: select("s")).grid(row=2, column=1, padx=5, pady=5)
        win.grab_set()

    #kollar om det finns varningar direkt vid spelets start
    checkSurroundingNodes()
    root.mainloop()