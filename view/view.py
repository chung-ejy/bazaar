import tkinter as tk

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Turn-Based Game")

        # Create a main frame to hold the sub-frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create a frame for equations with a black outline
        self.equation_frame = tk.Frame(self.main_frame, bg="black", borderwidth=2, relief="solid")
        self.equation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        
        # Create a frame for cards with a black outline
        self.card_frame = tk.Frame(self.main_frame, bg="black", borderwidth=2, relief="solid")
        self.card_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Create a frame for player colors with a black outline
        self.player_colors_frame = tk.Frame(self.main_frame, bg="black", borderwidth=2, relief="solid")
        self.player_colors_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Create a frame for player scores with a black outline
        self.player_scores_frame = tk.Frame(self.main_frame, bg="black", borderwidth=2, relief="solid")
        self.player_scores_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Create a canvas widget for equations
        self.equation_canvas = tk.Canvas(self.equation_frame, width=200, height=600, bg="white")
        self.equation_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create a canvas widget for cards
        self.card_canvas = tk.Canvas(self.card_frame, width=400, height=600, bg="white")
        self.card_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create a canvas widget for player colors
        self.player_colors_canvas = tk.Canvas(self.player_colors_frame, height=100, bg="white")
        self.player_colors_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create a canvas widget for player scores
        self.player_scores_canvas = tk.Canvas(self.player_scores_frame, height=100, bg="white")
        self.player_scores_canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Configure grid weights to ensure canvases expand with the window
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)

        self.equation_frame.grid_rowconfigure(0, weight=1)
        self.equation_frame.grid_columnconfigure(0, weight=1)

        self.card_frame.grid_rowconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(0, weight=1)

        self.player_colors_frame.grid_rowconfigure(0, weight=1)
        self.player_colors_frame.grid_columnconfigure(0, weight=1)

        self.player_scores_frame.grid_rowconfigure(0, weight=1)
        self.player_scores_frame.grid_columnconfigure(0, weight=1)

        # Initialize positions for cards and equations
        self.card_row_start = 0
        self.equation_row = 0
        self.card_canvas_height = self.card_canvas.winfo_reqheight()
        self.card_canvas_center_y = self.card_canvas_height // 2

    def draw_card(self, card):
        # Enlarged card size
        card_width, card_height = 150, 200
        color_height = 25
        smiley_size = 40

        # Calculate vertical position to center the card vertically in the canvas
        card_y = self.card_canvas_center_y - (card_height // 2)
        card_x = self.card_row_start * (card_width + 20) + 10
        
        # Draw the card
        self.card_canvas.create_rectangle(card_x, card_y, 
                                          card_x + card_width, card_y + card_height, 
                                          fill="lightgrey", outline="black")

        # Draw colors at the bottom of the card, ensuring they fit within the card width
        self.draw_card_color_field(card.cost, card_x + 10, card_y + card_height - color_height - 10, color_height, card_width - 20)

        # Draw smiley face if smiley is True
        if card.smiley:
            self.draw_smiley(card_x + card_width // 2, card_y + card_height // 2, smiley_size)

        # Update position for the next card
        self.card_row_start += 1

        # Reset column if necessary
        if self.card_row_start * (card_width + 20) + card_width > self.card_canvas.winfo_reqwidth():
            self.card_row_start = 0

    def draw_equation(self, equation):
        # Adjusted height for fitting more equations
        equation_width = 200
        equation_height = 60

        # Draw input colors
        self.draw_equation_color_field(equation.input, 10, self.equation_row * (equation_height + 10), equation_height // 2)

        # Draw output colors
        self.draw_equation_color_field(equation.output, 120, self.equation_row * (equation_height + 10), equation_height // 2)

        # Update position for the next equation
        self.equation_row += 1

        # Reset row if necessary
        if self.equation_row * (equation_height + 10) + equation_height > self.equation_canvas.winfo_reqheight():
            self.equation_row = 0

    def draw_card_color_field(self, colors, x, y, color_height, card_width):
        # Draw rectangles for each color on card, ensuring they fit within card width
        color_width = (card_width - 20) // len(colors)
        padding = 5
        
        for i, color in enumerate(colors):
            self.card_canvas.create_rectangle(
                x + i * (color_width + padding),
                y,
                x + i * (color_width + padding) + color_width,
                y + color_height,
                fill=color.value,
                outline="black"
            )

    def draw_equation_color_field(self, colors, x, y, color_height):
        # Draw rectangles for each color on equation
        color_width = 20
        padding = 5
        
        for i, color in enumerate(colors):
            self.equation_canvas.create_rectangle(
                x + i * (color_width + padding),
                y,
                x + i * (color_width + padding) + color_width,
                y + color_height,
                fill=color.value,
                outline="black"
            )

    def draw_smiley(self, x, y, size):
        # Draw a simplified smiley face as a yellow circle
        face_radius = size // 2
        
        # Draw face
        self.card_canvas.create_oval(
            x - face_radius,
            y - face_radius,
            x + face_radius,
            y + face_radius,
            fill="yellow",
            outline="black"
        )

    def draw_player_colors(self, colors):
        # Draw player colors in a horizontal line
        color_width = 30
        color_height = 30
        padding = 10

        # Calculate total width needed for colors
        total_width = len(colors) * (color_width + padding) - padding
        start_x = (self.player_colors_canvas.winfo_reqwidth() - total_width) // 2
        
        # Draw each color
        for i, color in enumerate(colors):
            self.player_colors_canvas.create_rectangle(
                start_x + i * (color_width + padding),
                10,
                start_x + i * (color_width + padding) + color_width,
                10 + color_height,
                fill=color.value,
                outline="black"
            )
    
    def draw_player_score(self, player_name, score):
        # Clear the canvas before drawing
        self.player_scores_canvas.delete("all")

        # Get the current width and height of the canvas to center the text
        canvas_width = self.player_scores_canvas.winfo_width()
        canvas_height = self.player_scores_canvas.winfo_height()

        # Draw the player's name and score in the center of the canvas
        text = f"{player_name}: {score}"
        self.player_scores_canvas.create_text(
            canvas_width // 2,  # X-coordinate at the center
            canvas_height // 2,  # Y-coordinate at the center
            text=text,
            font=("Arial", 16),
            fill="black"
        )
        
    def refresh(self):
        # Clear canvases
        self.card_canvas.delete("all")
        self.equation_canvas.delete("all")
        self.player_colors_canvas.delete("all")
        self.player_scores_canvas.delete("all")

        # Initialize positions for cards and equations
        self.card_row_start = 0
        self.equation_row = 0
        self.card_canvas_height = self.card_canvas.winfo_reqheight()
        self.card_canvas_center_y = self.card_canvas_height // 2
