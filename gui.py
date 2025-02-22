import tkinter as tk
from tkinter import messagebox
from classes import Entity
from nodeFunctions import getNode, getNodeItem, getRandomNode
from globalVariables import gameState

def guiLoop(player):
    root = tk.Tk()
    root.title("Wumpus")
    root.geometry("500x400")
    label = tk.Label(root, text=f"Aktuellt rum: {player.id}", font=("Arial", 16))
    label.pack(pady=20)
    def updateLabel():
        label.config(text=f"Aktuellt rum: {player.id}")
        root.update_idletasks()
        root.after(1000, updateLabel)
    updateLabel()
    root.mainloop()

def startGameGui(nodes, player, wumpus):
    arrowsLeft = 3 if gameState.difficulty == "3" else 5
    moves = 0
    root = tk.Tk()
    root.title("Wumpus GUI")
    root.geometry("600x400")
    messageText = tk.Text(root, height=10, width=70)
    messageText.pack(pady=10)
    roomLabel = tk.Label(root, text=f"Du befinnner dig i rum: {player.id}", font=("Arial", 16))
    roomLabel.pack(pady=5)
    buttonFrame = tk.Frame(root)
    buttonFrame.pack(pady=10)
    moveButton = tk.Button(buttonFrame, text="Rör dig", width=10, command=lambda: moveAction())
    shootButton = tk.Button(buttonFrame, text=f"Skjut ({arrowsLeft})", width=10, command=lambda: shootAction())
    mapButton = tk.Button(buttonFrame, text="Kolla kartan", width=10, command=lambda: mapAction())
    quitButton = tk.Button(buttonFrame, text="Avsluta", width=10, command=lambda: quitAction())
    moveButton.grid(row=0, column=0, padx=5)
    shootButton.grid(row=0, column=1, padx=5)
    mapButton.grid(row=0, column=2, padx=5)
    quitButton.grid(row=0, column=3, padx=5)
    
    state = {
        "arrowsLeft": arrowsLeft,
        "moves": moves,
        "player": player,
        "nodes": nodes,
        "wumpus": wumpus,
        "gameOver": False,
    }
    def appendMessage(msg):
        messageText.insert(tk.END, msg + "\n")
        messageText.see(tk.END)

    def updateRoomLabel():
        roomLabel.config(text=f"Aktuellt rum: {state['player'].id}")

    def checkGameOver():
        if state["gameOver"]:
            moveButton.config(state=tk.DISABLED)
            shootButton.config(state=tk.DISABLED)
            mapButton.config(state=tk.DISABLED)
            quitButton.config(state=tk.DISABLED)
    def displayWarnings():
        seen = set()
        messages = {}
        for direction in ["n", "e", "s", "w"]:
            adjacentNodeId = getattr(state["player"], direction)
            if adjacentNodeId in seen:
                continue
            seen.add(adjacentNodeId)
            nodeItem = getNodeItem(state["nodes"], adjacentNodeId)
            if nodeItem is not None and nodeItem.entityType != "N" and nodeItem.entityMessage:
                messages[nodeItem.entityMessage] = messages.get(nodeItem.entityMessage, 0) + 1
        for msg, count in messages.items():
            if count > 1:
                appendMessage(f"{msg} x{count}")
            else:
                appendMessage(msg)
    def moveAction():
        askDirection("Rör dig", "Välj riktning att gå:", processMoveDirection)
    def processMoveDirection(direction):
        state["moves"] += 1
        targetNodeId = getattr(state["player"], direction)
        if targetNodeId is None:
            appendMessage("Det finns ingen dörr i den riktningen!")
            return
        collisionItem = getNodeItem(state["nodes"], targetNodeId)
        if collisionItem is None:
            appendMessage("Rummet i den riktningen existerar inte!")
            return
        if collisionItem.entityType == "N":
            currentNode = getNode(state["nodes"], state["player"].id)
            currentNode.item = Entity(currentNode.id, "N")
            newPlayerNode = getNode(state["nodes"], targetNodeId)
            newPlayerNode.item = Entity(newPlayerNode.id, "P")
            state["player"] = newPlayerNode
            appendMessage(f"Du gick in i rum: {newPlayerNode.id}.")
            updateRoomLabel()
            displayWarnings()
        else:
            processCollision(collisionItem.entityType)
        checkGameOver()
    def processCollision(collisionType):
        if collisionType == "W":
            appendMessage("Du blev uppäten av Wumpus...")
            endGame(False)
        elif collisionType == "H":
            appendMessage("Du föll ner i ett bottenlöst hål...")
            endGame(False)
        elif collisionType == "B":
            appendMessage("Fladdermöss lyfter upp dig!")
            currentNode = getNode(state["nodes"], state["player"].id)
            currentNode.item = Entity(currentNode.id, "N")
            newNode = getRandomNode(state["nodes"])
            while getNodeItem(state["nodes"], newNode.id).entityType != "N":
                newNode = getRandomNode(state["nodes"])
            newNode.item = Entity(newNode.id, "P")
            state["player"] = newNode
            appendMessage(f"Du landade i rum: {newNode.id}.")
            updateRoomLabel()
            displayWarnings()
    def shootAction():
        if state["arrowsLeft"] < 1:
            appendMessage("Du fick slut på pilar! Du förlorade!")
            endGame(False)
            return
        state["arrowsLeft"] -= 1
        state["moves"] += 1
        arrowRoomId = state["player"].id
        shootArrowStep(1, arrowRoomId)

    def shootArrowStep(step, arrowRoomId):
        if step > 3:
            appendMessage("Pilen missade Wumpus.")
            return
        appendMessage(f"Pilen befinner sig i rum {arrowRoomId} (steg {step}).")
        askDirection("Skjut", "Välj riktning för pilen:", lambda d: processShootStep(step, arrowRoomId, d))

    def processShootStep(step, arrowRoomId, direction):
        currentArrowNode = getNode(state["nodes"], arrowRoomId)
        newArrowRoomId = getattr(currentArrowNode, direction)
        appendMessage(f"Pilen flyttas till rum: {newArrowRoomId}.")
        roomItem = getNodeItem(state["nodes"], newArrowRoomId)
        if roomItem.entityType == "W":
            appendMessage("Du träffade Wumpus med pilen!")
            endGame(True)
            return
        else:
            shootArrowStep(step + 1, newArrowRoomId)

    def mapAction():
        mapWin = tk.Toplevel(root)
        mapWin.title("Karta")
        text = tk.Text(mapWin, height=10, width=50)
        text.pack()
        cols = 4
        for i, node in enumerate(state["nodes"]):
            text.insert(tk.END, f"{node.item.entityType} ")
            if (i+1) % cols == 0:
                text.insert(tk.END, "\n")
        text.config(state=tk.DISABLED)

    def quitAction():
        appendMessage("Spelet är över. Du avslutade.")
        endGame(False)

    def endGame(won):
        state["gameOver"] = True
        if won:
            recordMessage = ""
            try:
                with open("highscore.txt", "r+") as file:
                    content = file.read().strip()
                    if content:
                        highscore = int(content)
                    else:
                        highscore = None
                    if highscore is None or state["moves"] < highscore:
                        if highscore is not None:
                            recordMessage = f"Du slog ditt tidigare rekord på {highscore} drag!"
                        else:
                            recordMessage = "Detta är ditt första rekord!"
                        file.seek(0)
                        file.write(str(state["moves"]))
                        file.truncate()
                    else:
                        recordMessage = f"Ditt bästa rekord är {highscore} drag."
            except Exception as e:
                recordMessage = "Rekord kunde inte uppdateras."
            msg = f"Grattis, du vann på {state['moves']} drag!\n{recordMessage}"
        else:
            msg = f"Spelet är över! Du förlorade efter {state['moves']} drag."
        appendMessage(msg)
        checkGameOver()
        messagebox.showinfo("Spelet är över", msg)
        root.destroy()

    def askDirection(title, prompt, callback):
        win = tk.Toplevel(root)
        win.title(title)
        tk.Label(win, text=prompt).pack(pady=10)
        btnFrame = tk.Frame(win)
        btnFrame.pack(pady=5)
        def select(direction):
            callback(direction)
            win.destroy()
        tk.Button(btnFrame, text="Norr", width=10, command=lambda: select("n")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btnFrame, text="Väst", width=10, command=lambda: select("w")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btnFrame, text="Öster", width=10, command=lambda: select("e")).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(btnFrame, text="Söder", width=10, command=lambda: select("s")).grid(row=2, column=1, padx=5, pady=5)
        win.grab_set()
    displayWarnings()
    root.mainloop()