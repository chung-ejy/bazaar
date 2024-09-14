from components.action import Action
from components.utils import Utils
import sys
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def setup(self):
        self.model.setup()
    
    def render(self):
        self.view.refresh()
        for card in self.model.board.fieldcards:
            self.view.draw_card(card)
        for equation in self.model.board.equations:
            self.view.draw_equation(equation)
        self.view.draw_player_colors(self.model.player.pebbles)
        self.view.draw_player_score(self.model.player.name,self.model.player.score)
        self.view.save_as_png("state.png")
    
    def live(self):
        return self.model.referee.live(self.model.board)
    
    def turn(self,input):
        action = Utils.extract_json_objects(input)[0]
        try:
            if action == f"{Action.DRAW.value}":
                self.model.referee.draw(self.model.board,self.model.player)
            elif action == f"{Action.EXCHANGE.value}":
                query = Utils.extract_json_objects(input)[1]
                self.model.referee.exchange(query,self.model.board,self.model.player)
            elif action == f"{Action.PURCHASE.value}":
                query = Utils.extract_json_objects(input)[1]
                self.model.referee.purchase(query,self.model.board,self.model.player)
                self.model.referee.score(self.model.player)
            elif action == f"{Action.END.value}":
                sys.exit()
            else:
                print("invalid command")
        except Exception as e:
            print(str(e))
