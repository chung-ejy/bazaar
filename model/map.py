from components.board import Board

class Map(object):

    def __init__(self,referee,player):
        self.referee = referee
        self.player = player
    
    def setup(self):
        self.board = Board(self.referee.initialize_bank()
                           ,self.referee.initialize_fieldcards()
                           ,self.referee.initialize_deck()
                           ,self.referee.initialize_equations())
    