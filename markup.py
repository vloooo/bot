from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from callback import CallbackDataFactory


class MarkupFactory:
    def __init__(self, rows, callback=''):
        self.callback_prefix = callback
        self.rows = rows

    def build(self):
        if self.callback_prefix:
            markup = InlineKeyboardMarkup()
            keyboard_type = InlineKeyboardButton
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard_type = KeyboardButton

        row_buttons = []
        for row in self.rows:
            for btn_text in row:
                if btn_text == 'Oтправить контакт':
                    row_buttons.append(keyboard_type(btn_text, request_contact=True))
                elif self.callback_prefix:
                    callback = CallbackDataFactory({self.callback_prefix: btn_text})
                    row_buttons.append(keyboard_type(btn_text, callback_data=callback.str))
                else:
                    row_buttons.append(keyboard_type(btn_text))
            markup.row(*row_buttons)
            row_buttons.clear()
        return markup
