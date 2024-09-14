from components.board import Board

class Map(object):

    def __init__(self,referee,players):
        self.referee = referee
        self.players = players
    
    def setup(self):
        self.board = Board(self.referee.initialize_bank()
                           ,self.referee.initialize_fieldcards()
                           ,self.referee.initialize_deck()
                           ,self.referee.initialize_equations())
        self.turn = 0
        self.active_player_index = self.turn % len(self.players)
    
    def change_player(self):
        self.active_player_index = self.turn % len(self.players)