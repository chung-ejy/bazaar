from PIL import Image, ImageDraw, ImageFont

class View:
    def __init__(self):
        # Create a blank image to draw on
        self.width, self.height = 800, 600  # Size of the image
        self.image = Image.new("RGB", (self.width, self.height), color="white")
        self.draw = ImageDraw.Draw(self.image)

        # Load a font for text (default if none available)
        try:
            self.font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            self.font = ImageFont.load_default()

        # Initialize positions for cards and equations
        self.card_row_start = 0
        self.equation_row = 0

    def draw_card(self, card):
        card_width, card_height = 150, 200
        color_height = 25
        smiley_size = 40

        # Calculate vertical position to center the card vertically in the image
        card_y = (self.height // 2) - (card_height // 2)
        card_x = self.card_row_start * (card_width + 20) + 10

        # Draw the card rectangle
        self.draw.rectangle(
            [card_x, card_y, card_x + card_width, card_y + card_height],
            fill="lightgrey",
            outline="black"
        )

        # Draw colors at the bottom of the card
        self.draw_card_color_field(card.cost, card_x + 10, card_y + card_height - color_height - 10, color_height, card_width - 20)

        # Draw smiley face if smiley is True
        if card.smiley:
            self.draw_smiley(card_x + card_width // 2, card_y + card_height // 2, smiley_size)

        # Update position for the next card
        self.card_row_start += 1

    def draw_equation(self, equation):
        equation_width = 200
        equation_height = 60

        # Draw input colors
        self.draw_equation_color_field(equation.input, 10, self.equation_row * (equation_height + 10), equation_height // 2)

        # Draw output colors
        self.draw_equation_color_field(equation.output, 120, self.equation_row * (equation_height + 10), equation_height // 2)

        # Update position for the next equation
        self.equation_row += 1

    def draw_card_color_field(self, colors, x, y, color_height, card_width):
        color_width = (card_width - 20) // len(colors)
        padding = 5

        for i, color in enumerate(colors):
            self.draw.rectangle(
                [x + i * (color_width + padding), y, x + i * (color_width + padding) + color_width, y + color_height],
                fill=color.value,
                outline="black"
            )

    def draw_equation_color_field(self, colors, x, y, color_height):
        color_width = 20
        padding = 5

        for i, color in enumerate(colors):
            self.draw.rectangle(
                [x + i * (color_width + padding), y, x + i * (color_width + padding) + color_width, y + color_height],
                fill=color.value,
                outline="black"
            )

    def draw_smiley(self, x, y, size):
        # Draw a simplified smiley face as a yellow circle
        face_radius = size // 2
        self.draw.ellipse(
            [x - face_radius, y - face_radius, x + face_radius, y + face_radius],
            fill="yellow",
            outline="black"
        )

    def draw_player_colors(self, colors):
        color_width = 30
        color_height = 30
        padding = 10

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
        # Save the image as PNG
        self.image.save(filename)

    def refresh(self):
        # Clear the image for new drawings
        self.image = Image.new("RGB", (self.width, self.height), color="white")
        self.draw = ImageDraw.Draw(self.image)
        self.card_row_start = 0
        self.equation_row = 0
