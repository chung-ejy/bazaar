from server.server import Server
from components.referee import Referee
from components.player import Player
from components.ai_player import AIPlayer
from view.view import View
from model.map import Map
from controller.controller import Controller
import sys
import time
import json
from components.utils import Utils
class App:
    
    def __init__(self):
        self.server = Server()
        self.signup = True
        # self.player = Player("eric")
    
    def run(self):
        self.server.start_server()
        players = []
        while self.signup == True:
            # Check if there's input from the server
            commands = Utils.extract_json_objects(self.server.receive())
            if len(commands) > 0:
                for command in commands:
                    players.append(command["name"])
                    print(command["name"],"has joined the game")
            self.server.clear_queue()
            if len(players) > 0:
                self.signup = False
        player_classes = [Player(x) for x in players]
        player_classes.append(AIPlayer("ai"))
        model = Map(Referee(),player_classes)
        view = View()  # No view component since we're not using a GUI
        controller = Controller(model,view)
        controller.setup()
        while controller.model.referee.live(controller.model.board) == True:
            active_player = controller.model.players[controller.model.turn % len(controller.model.players)]
            commands = [active_player.move()] if active_player.isai == True else Utils.extract_json_objects(self.server.receive()) 
            if len(commands) > 0:
                for command in commands:
                    controller.turn(command)
                controller.render()
                controller.model.turn += 1
                controller.change_player()
                print(controller.model.turn,controller.model.active_player_index)
        self.server.close()
