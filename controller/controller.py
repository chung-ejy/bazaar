from components.action import Action

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
        self.view.draw_player_colors(self.model.players[self.model.active_player_index].pebbles)
        self.view.draw_player_score(self.model.players[self.model.active_player_index].name,self.model.players[self.model.active_player_index].score)
        self.view.save_as_png("state.png")
    
    def live(self):
        return self.model.referee.live(self.model.board,self.model.players)
    
    def turn(self,input):
        action = input["action"]
        query = input["query"]
        try:
            if action == f"{Action.DRAW.value}":
                self.model.referee.draw(self.model.board,self.model.players[self.model.active_player_index])
                return
            elif action == f"{Action.EXCHANGE.value}":
                if self.model.referee.legal_exchange(query,self.model.board,self.model.players[self.model.active_player_index]):
                    self.model.referee.exchange(query,self.model.board,self.model.players[self.model.active_player_index])
                else:
                    print("invalid exchange")
            elif action == f"{Action.PURCHASE.value}":
                if self.model.referee.legal_purchase(query,self.model.board,self.model.players[self.model.active_player_index]):
                    card = self.model.referee.purchase(query,self.model.board,self.model.players[self.model.active_player_index])
                    self.model.referee.score(self.model.players[self.model.active_player_index], card)
                else:
                    print("invalid purchase")
            elif action == f"{Action.END.value}":
                return
            else:
                print("invalid command")
        except Exception as e:
            print(str(e))
        
    def change_player(self):
        self.model.change_player()
