from server.server import Server
from components.referee import Referee
from components.player import Player
from view.view import View
from model.map import Map
from controller.controller import Controller
import sys
import time
import json
class App:
    def __init__(self):
        self.server = Server()
        self.server.start_server()
        self.referee = Referee("Joe", 5, 10, 4, 100)
        self.player = Player("eric")
        self.model = Map(self.referee, self.player)
        self.view = View()  # No view component since we're not using a GUI
        self.controller = Controller(self.model, self.view)
        self.controller.setup()

    def run(self):
        while True:
            # Check if there's input from the server
            input_data = self.server.receive()
            if input_data:
                self.controller.turn(input_data)
                self.controller.render()

if __name__ == "__main__":
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)
