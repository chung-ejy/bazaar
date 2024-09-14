from components.referee import Referee
from components.player import Player
from model.map import Map
from view.view import View
from controller.controller import Controller  # Import the new Controller class
import tkinter as tk
import sys
if __name__ == "__main__":

    referee = Referee("Joe",5,10,4,100)
    player = Player("eric")
    model = Map(referee, player)
    root = tk.Tk()
    view = View(root)
    controller = Controller(model, view)  # Initialize the controller
    controller.setup()
    while controller.live():
        controller.render()
        controller.turn()
    root.mainloop()
    sys.exit()
