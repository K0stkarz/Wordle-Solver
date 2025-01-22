from . import TextInput

class LimitedTextInput(TextInput):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < 1 and substring.isalpha():
            super().insert_text(substring, from_undo=from_undo)
            self.app_instance.on_letter_input(self)
            next_index = self.index + 1
            if next_index < len(self.app_instance.letter_inputs):
                self.app_instance.letter_inputs[next_index].focus = True

    def do_backspace(self, from_undo=False, mode='bkspc'):
        old_text = self.text
        super().do_backspace(from_undo, mode)
        
        # Sprawdzamy czy tekst został usunięty
        if old_text and not self.text:
            self.app_instance.on_letter_delete(self)
            prev_index = self.index - 1
            if prev_index >= 0:
                self.app_instance.letter_inputs[prev_index].focus = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Obsługa Ctrl+A
        if keycode[1] == 'a' and 'ctrl' in modifiers:
            self.select_all()
            return True
            
        # Obsługa Delete/Backspace gdy tekst jest zaznaczony
        if keycode[1] in ('delete', 'backspace') and self.selection_text == self.text:
            old_text = self.text
            self.text = ''
            if old_text:
                self.app_instance.on_letter_delete(self)
                prev_index = self.index - 1
                if prev_index >= 0:
                    self.app_instance.letter_inputs[prev_index].focus = True
            return True

        # Obsługa Tab
        if keycode[1] == 'tab':
            next_index = self.index + 1
            if next_index < len(self.app_instance.letter_inputs):
                self.app_instance.letter_inputs[next_index].focus = True
            return True
            
        return super().keyboard_on_key_down(window, keycode, text, modifiers)