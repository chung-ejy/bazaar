from .pebble import Pebble
class Player(object):

    def __init__(self,name):
        self.name = name
        self.pebbles = {}
        self.score = 0
        self.isai = False
    
    def draw(self,pebble):
        if pebble in self.pebbles.keys():
            self.pebbles[pebble] +=1
        else:
            self.pebbles[pebble] = 1
