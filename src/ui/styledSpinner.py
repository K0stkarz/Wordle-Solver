from . import Spinner, COLORS, FONTS, dp, Color, RoundedRectangle, DropDown, Button

class StyledSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS["secondary"]
        self.font_name = FONTS["medium"]
        self.font_size = dp(18)

        with self.canvas.before:
            Color(*COLORS["primary"])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(8)])

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.option_cls = self.create_option()
        self.dropdown_cls = self.RoundedDropdown

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    class RoundedDropdown(DropDown):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.background_color = COLORS["surface"]
            self.border = [0, 0, 0, 0]
            self.max_height = dp(200)

            with self.canvas.before:
                Color(*COLORS["surface"])
                self.bg_rect = RoundedRectangle(radius=[dp(8)])

            self.bind(pos=self.update_bg, size=self.update_bg)

        def update_bg(self, instance, value):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    def create_option(self):
        class RoundedOption(Button):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_normal = ""
                self.background_color = COLORS["surface"]
                self.color = COLORS["text"]
                self.font_name = FONTS["regular"]
                self.size_hint_y = None
                self.height = dp(40)

                with self.canvas.before:
                    Color(*COLORS["surface"])
                    self.rect = RoundedRectangle(
                        pos=self.pos, size=self.size, radius=[dp(4)]
                    )

                self.bind(pos=self.update_rect, size=self.update_rect)

            def update_rect(self, instance, value):
                self.rect.pos = self.pos
                self.rect.size = self.size

        return RoundedOption