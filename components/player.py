from .pebble import Pebble
class Player(object):

    def __init__(self,name):
        self.name = name
        self.pebbles = [Pebble.BLUE]
        self.cards = []
        self.score = 0
    
    def draw(self,pebble):
        self.pebbles.append(pebble)
