import random

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

class Entity:
    def __init__(self, position, entityType):
        self.position = position
        self.entityType = entityType
    def __str__(self):
        return self.entityType
       

class GameState:
    def __init__(self):
        self.gameOver = False