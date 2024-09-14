from server.server import Server
from components.referee import Referee
from components.player import Player
from model.map import Map
from view.view import View
from controller.controller import Controller  # Import the new Controller class
import tkinter as tk
import sys

class App:
    def __init__(self, root):
        self.server = Server()
        self.server.start_server()
        self.referee = Referee("Joe", 5, 10, 4, 100)
        self.player = Player("eric")
        self.model = Map(self.referee, self.player)
        self.view = View(root)
        self.controller = Controller(self.model, self.view)
        self.controller.setup()
        self.root = root

    def check_server_input(self):
        try:
            # Check if there's input from the server
            input_data = self.server.receive()
            if input_data:
                # Process the input data with the controller
                self.controller.turn(input_data)
                self.controller.render()  # Update the view if needed
        except Exception as e:
            print(f"Error during server input handling: {e}")

        # Schedule the next server check (in milliseconds)
        self.root.after(100, self.check_server_input)

if __name__ == "__main__":
    root = tk.Tk()

    # Initialize the app and schedule the server input check
    app = App(root)
    app.check_server_input()

    # Start the Tkinter main loop
    root.mainloop()

    # Clean up before exiting
    sys.exit(0)
