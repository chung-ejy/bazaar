from .player import Player

class AIPlayer(Player):

    def __init__(self,name):
        super().__init__(name)
        self.isai = True
    
    def move(self):
        return "DRAW"