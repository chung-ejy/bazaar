from random import randint, choice
from .pebble import Pebble
from .equation import Equation
from .card import Card
from math import prod

class Referee(object):

    def __init__(self,name,num_equations=10,cards_in_deck=20,cards_in_field=4,num_of_pebbles=100):
        self.name = name
        self.num_equations = num_equations
        self.cards_in_deck = cards_in_deck
        self.cards_in_field = cards_in_field
        self.num_of_pebbles = num_of_pebbles
    
    def initialize_equations(self):
        equations = []
        for i in range(self.num_equations):
            left_num_colors = randint(1,4)
            right_num_colors = randint(1,4)
            left_colors = []
            right_colors = []
            for i in range(left_num_colors):
                left_colors.append(choice(list(Pebble)))
            for i in range(right_num_colors):
                right_colors.append(choice(list(Pebble)))
            equations.append(Equation(left_colors,right_colors))
        return equations
    
    def initialize_deck(self):
        cards = []
        for i in range(self.cards_in_deck):
            cost = [choice(list(Pebble)) for i in range(5)]
            smiley = choice([True,False])
            card = Card(cost,smiley)
            cards.append(card)
        return cards
    
    def initialize_fieldcards(self):
        cards = []
        for i in range(self.cards_in_field):
            cost = [choice(list(Pebble)) for i in range(5)]
            smiley = choice([True,False])
            card = Card(cost,smiley)
            cards.append(card)
        return cards
    
    def initialize_bank(self):
        bank = []
        for i in range(self.num_of_pebbles):
            bank.append(choice(list(Pebble)))
        return bank

    def live(self,board):
        return 0 != prod([len(board.bank) > 0, len(board.fieldcards) > 0])
    
    def draw(self,board,player):
        pebble = board.bank.pop(-1)
        player.draw(pebble)
    
    def exchange(self,query,board,player):
        equation = board.equations[query["equation"]]
        try:
            for input in equation.input:
                player.pebbles.remove(input)
            for output in equation.output:
                board.bank.remove(output)
                player.draw(output)
        except:
            print("invalid exchange")

    def purchase(self,query,board,player):
        card = board.fieldcards[query["card"]]
        inputs = card.cost
        try:
            for input in inputs:
                print(input)
                player.pebbles.remove(input)
            board.fieldcards.pop(query["card"])
            board.fieldcards.append(board.deck.pop(-1))
        except Exception as e:
            print(str(e))
            print("invalid purchase")
    
    def score(self,player):
        player.score += len(player.pebbles) / 3