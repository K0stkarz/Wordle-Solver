from . import TextInput, COLORS, FONTS, dp

class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_disabled_normal = ""
        self.background_color = COLORS["surface"]  # Nadpisuje styl disabled
        self.foreground_color = COLORS["primary"]
        self.hint_text_color = COLORS["primary"]
        self.font_name = FONTS["regular"]
        self.font_size = dp(16)
        self.padding = [dp(8), dp(8)]
        self.cursor_color = COLORS["secondary"]
        self.cursor_width = dp(2)