#Alla rum i spelet är en nod
class Node: 
    def __init__(self,id, item, n, e, s, w):
        self.id = id
        self.item = item
        self.n = n
        self.e = e
        self.s = s
        self.w = w
    def __str__(self):
        return f"id: {self.id} item:{str(self.item)} w: {self.w} n: {self.n} s: {self.s} e: {self.e}"

#alla rum/noder innehåller en Entity. Entity kan vara tom eller inehålla ett spelobjekt
class Entity:
    def __init__(self, position, entityType, entityMessage = ""):
        self.position = position
        self.entityType = entityType
        self.entityMessage = entityMessage 
    def __str__(self):
        return self.entityType
       
#spara spelets status, svårighetsgrad och om spelet är över
class GameState:
    def __init__(self, difficulty = "1"):
        self.gameOver = False
        self.difficulty = difficulty