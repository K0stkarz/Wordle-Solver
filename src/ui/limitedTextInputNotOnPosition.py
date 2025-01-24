from . import TextInput


class LimitedTextInputNotOnPosition(TextInput):
    def __init__(self, app_instance, max_length, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.max_length = max_length

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_length:
            substring = substring[: self.max_length - len(self.text)]
        if len(self.text) < self.max_length and substring.isalpha():
            super().insert_text(substring, from_undo=from_undo)
            self.app_instance.on_letter_input_not_on_pos(self, to_add=substring)
            if len(self.text) == self.max_length:
                next_index = (
                    self.index + 1 + int((len(self.app_instance.letter_inputs) / 2))
                )
                if next_index < len(self.app_instance.letter_inputs):
                    self.app_instance.letter_inputs[next_index].focus = True

    def do_backspace(self, from_undo=False, mode="bkspc"):
        old_text = self.text[len(self.text) - 1]
        super().do_backspace(from_undo, mode)

        self.app_instance.on_letter_delete_not_on_pos(self, to_del=old_text)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == "a" and "ctrl" in modifiers:
            self.select_all()
            return True

        # Obsługa Delete/Backspace gdy tekst jest zaznaczony
        if keycode[1] in ("delete", "backspace") and self.selection_text == self.text:
            old_text = self.text
            self.text = ""
            if old_text:
                self.app_instance.on_letter_delete(self)

            return True

        # Obsługa Tab
        if keycode[1] == "tab":
            next_index = self.index + 1 + int(len(self.app_instance.letter_inputs) / 2)
            if next_index < len(self.app_instance.letter_inputs):
                self.app_instance.letter_inputs[next_index].focus = True
            else:
                self.app_instance.letter_inputs[0].focus = True
            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)
