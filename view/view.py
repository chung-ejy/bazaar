from PIL import Image, ImageDraw, ImageFont

class View:
    def __init__(self):
        self.width, self.height = 800, 600  # Initial size of the image
        self.image = Image.new("RGB", (self.width, self.height), color="white")
        self.draw = ImageDraw.Draw(self.image)

        # Load a font for text
        try:
            self.font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            self.font = ImageFont.load_default()

        # Layout parameters
        self.header_height = 100  # Space for player information (score and colors)
        self.card_area_height = 200  # Reduced space allocated for cards
        self.equation_area_start = self.header_height + self.card_area_height  # Equations start after cards
        self.padding = 10  # Reduced padding for compact layout

        # Initialize positions for cards and equations
        self.card_row_start = 0
        self.card_start_y = self.header_height + self.padding  # Cards start below header
        self.equation_start_y = self.equation_area_start + self.padding
        self.equation_row = 0
        self.max_equation_rows = 5

    def extend_canvas_if_needed(self, current_y):
        """Extend the canvas height if the content exceeds the current image height."""
        if current_y + self.padding > self.height:
            new_height = current_y + self.padding
            new_image = Image.new("RGB", (self.width, new_height), color="white")
            new_image.paste(self.image, (0, 0))
            self.image = new_image
            self.draw = ImageDraw.Draw(self.image)
            self.height = new_height

    def draw_card(self, card):
        card_width, card_height = 100, 130  # Reduced card size
        color_height = 15  # Reduced color block size
        smiley_size = 30  # Reduced smiley face size

        # Calculate total width of all cards to center them
        total_card_width = (card_width + self.padding) * 4 - self.padding  # Assume max 4 cards per row
        start_x = (self.width - total_card_width) // 2

        # Calculate the x and y position for the card
        card_y = self.card_start_y
        card_x = start_x + self.card_row_start * (card_width + self.padding)

        # Check if the card exceeds the image width and needs a new row
        if self.card_row_start == 4:  # New row after 4 cards
            self.card_row_start = 0
            card_x = start_x
            self.card_start_y += card_height + self.padding
            card_y = self.card_start_y

        # Draw the card rectangle
        self.draw.rectangle(
            [card_x, card_y, card_x + card_width, card_y + card_height],
            fill="lightgrey",
            outline="black"
        )

        # Draw colors at the bottom of the card
        self.draw_card_color_field(card.cost, card_x + 5, card_y + card_height - color_height - 5, color_height, card_width - 10)

        # Draw smiley face if smiley is True
        if card.smiley:
            self.draw_smiley(card_x + card_width // 2, card_y + card_height // 2, smiley_size)

        # Update position for the next card
        self.card_row_start += 1

        # Ensure the image size accommodates the new row of cards
        self.extend_canvas_if_needed(card_y + card_height)

    def draw_equation(self, equation):
        equation_width = 150  # Reduced width for equations
        equation_height = 40  # Reduced height for equations
        col_padding = 80  # Space between the two columns

        # Calculate the vertical position for the equation
        column = self.equation_row // self.max_equation_rows  # Determine which column (0 or 1)
        row_in_column = self.equation_row % self.max_equation_rows  # Position within the column
        equation_y = self.equation_start_y + row_in_column * (equation_height + self.padding)
        equation_x = 10 + column * (equation_width + col_padding)

        # Draw input colors
        self.draw_equation_color_field(equation.input, equation_x, equation_y, equation_height // 2)

        # Draw output colors
        self.draw_equation_color_field(equation.output, equation_x + equation_width // 2 + 5, equation_y, equation_height // 2)

        # Update position for the next equation
        self.equation_row += 1

        # Ensure the image size accommodates more than 5 rows
        self.extend_canvas_if_needed(equation_y + equation_height)

    def draw_card_color_field(self, colors, x, y, color_height, card_width):
        color_width = (card_width - 10) // len(colors)
        padding = 3

        for i, color in enumerate(colors):
            self.draw.rectangle(
                [x + i * (color_width + padding), y, x + i * (color_width + padding) + color_width, y + color_height],
                fill=color.value,
                outline="black"
            )

    def draw_equation_color_field(self, colors, x, y, color_height):
        color_width = 15  # Reduced color block size for equations
        padding = 3

        for i, color in enumerate(colors):
            self.draw.rectangle(
                [x + i * (color_width + padding), y, x + i * (color_width + padding) + color_width, y + color_height],
                fill=color.value,
                outline="black"
            )

    def draw_smiley(self, x, y, size):
        face_radius = size // 2
        self.draw.ellipse(
            [x - face_radius, y - face_radius, x + face_radius, y + face_radius],
            fill="yellow",
            outline="black"
        )

    def draw_player_colors(self, colors):
        color_width = 20  # Reduced size for player colors
        color_height = 20
        padding = 5

        start_x = (self.width - (len(colors) * (color_width + padding))) // 2

        for i, color in enumerate(colors):
            self.draw.rectangle(
                [start_x + i * (color_width + padding), 10, start_x + i * (color_width + padding) + color_width, 10 + color_height],
                fill=color.value,
                outline="black"
            )

    def draw_player_score(self, player_name, score):
        text = f"{player_name}: {score}"
        self.draw.text(
            (self.width // 2, 50),
            text,
            font=self.font,
            fill="black",
            anchor="mm"  # Centered text
        )

    def save_as_png(self, filename):
        self.image.save(filename)

    def refresh(self):
        self.image = Image.new("RGB", (self.width, self.height), color="white")
        self.draw = ImageDraw.Draw(self.image)
        self.card_row_start = 0
        self.equation_row = 0
        self.card_start_y = self.header_height + self.padding
        self.equation_start_y = self.equation_area_start + self.padding
