import tkinter as tk

root = tk.Tk()
root.title("Wumpus")
root.geometry("500x400")

# Create a label for the player's room
label = tk.Label(root, text="Waiting for game...", font=("Arial", 16))
label.pack(pady=20)

def guiLoop(player):
    """Update the label dynamically"""
    playerRoom = player.id
    label.config(text=f"Player is in room {playerRoom}")  # Update the text
    root.update_idletasks()  # Force UI update

root.mainloop()  # Keep window running