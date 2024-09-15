from random import randint, choice
from .pebble import Pebble
from .equation import Equation
from .card import Card
from math import prod
from collections import Counter
class Referee(object):

    def __init__(self,num_equations=10,cards_in_deck=20,cards_in_field=4,num_of_pebbles=100):
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
        bank = {}
        for i in range(self.num_of_pebbles):
            pebble = choice(list(Pebble))
            if pebble in bank.keys():
                bank[pebble] += 1
            else:
                bank[pebble] = 1
        return bank

    def live(self,board,players):
        return len(board.deck) > 0 and 0 != prod([player.score < 20 for player in players])  
    
    def draw(self,board,player):
        pebble = choice(list(board.bank.keys()))
        board.bank[pebble] += -1
        player.draw(pebble)
    
    def exchange(self,query,board,player):
        equation = board.equations[query['equation']]
        for input in equation.input:
            player.pebbles[input] += -1
        for output in equation.output:
            board.bank[output] += -1
            player.draw(output)

    def legal_exchange(self,query,board,player):
        equation = board.equations[query['equation']]
        inputs = dict(Counter(equation.input))
        outputs = dict(Counter(equation.output))
        legal = True
        for color in inputs.keys():
            legal = color in player.pebbles.keys() and player.pebbles[color] >= inputs[color]
            if legal == False:
                return False
            else:
                continue
        for color in outputs.keys():
            legal = color in board.bank.keys() and board.bank[color] >= outputs[color]
            if legal == False:
                return False
            else:
                continue
        return legal
    
    def purchase(self,query,board,player):
        card = board.fieldcards[query['card']]
        inputs = card.cost
        try:
            for input in inputs:
                player.pebbles[input] += -1
            board.fieldcards.pop(query['card'])
            board.fieldcards.append(board.deck.pop(-1))
            return card
        except Exception as e:
            print(str(e))
            print("invalid purchase")
    
    def legal_purchase(self,query,board,player):
        card = board.fieldcards[query['card']]
        cost = dict(Counter(card.cost))
        legal = True
        for color in cost.keys():
            if color not in player.pebbles.keys() or player.pebbles[color] < cost[color]:
                return False
        return legal
    
    def score(self,player,card):
        if sum(player.pebbles.values()) > 3:
            player.score += 2 if card.smiley else 1
        elif sum(player.pebbles.values()) > 2:
            player.score +=  3 if card.smiley else 2
        elif sum(player.pebbles.values()) > 1:
            player.score +=  5 if card.smiley else 3
        else:
            player.score +=  8 if card.smiley else 5
        