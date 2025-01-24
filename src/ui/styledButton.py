from . import Button, COLORS, FONTS, Color, dp, RoundedRectangle   

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS["secondary"]
        self.font_name = FONTS["medium"]
        self.font_size = dp(18)
        self.bold = False
        with self.canvas.before:
            Color(*COLORS["primary"])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(8)])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size