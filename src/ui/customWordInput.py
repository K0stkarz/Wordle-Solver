from . import TextInput


class CustomWordInput(TextInput):
    def __init__(self, app_instance, input_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.input_callback = input_callback
        self.delete_callback = delete_callback
        self.last_text = ""
        self.select_text_on_delete = False

    def insert_text(self, substring, from_undo=False):
        super().insert_text(substring, from_undo=from_undo)
        if self.text != self.last_text:  # Tylko jeśli tekst się zmienił
            self.input_callback(self, self.text)
            self.last_text = self.text

    def do_backspace(self, from_undo=False, mode="bkspc"):
        old_text = self.text
        super().do_backspace(from_undo, mode)

        # Sprawdzamy czy tekst został całkowicie usunięty (np. przez Ctrl+A + Backspace)
        if old_text and not self.text:
            self.delete_callback(self)
        # Sprawdzamy czy tekst się zmienił i czy nie jest to usuwanie zaznaczonego tekstu
        elif old_text != self.text and not self.selection_text:
            self.delete_callback(self)

        self.last_text = self.text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == "a" and "ctrl" in modifiers:
            self.select_all()
            return True

        # Obsługa Delete gdy tekst jest zaznaczony
        if keycode[1] in ("delete", "backspace") and self.selection_text == self.text:
            old_text = self.text
            self.text = ""
            if old_text != self.text:
                self.delete_callback(self)
            return True

        return super().keyboard_on_key_down(window, keycode, text, modifiers)
