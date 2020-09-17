from callback import CallbackDataFactory
from const import tb, PHOTO_DIR
from markup import MarkupFactory


def get_callback_str(script, message, extra_callback):
    prev_data = getattr(message, 'data', None)
    if extra_callback:
        extra_callback = f"{CallbackDataFactory({'type': extra_callback}).str},"
    if prev_data and 'type' in prev_data:
        extra_callback = CallbackDataFactory(prev_data).get_type()

    return f"{extra_callback}{script.callback}" if script.callback else None


def simple_callback(script, message, extra_callback=''):
    callback_str = get_callback_str(script, message, extra_callback)

    if script.prev_question:
        edit_message(get_edit_marcup(message, script.prev_callback), script.prev_question, message)
    answer_markup = MarkupFactory(script.rows, callback=callback_str).build() if script.rows else script.markup
    tb.send_message(message.from_user.id, script.question, reply_markup=answer_markup)


def send_photo(name, message):
    photo = open(f'{PHOTO_DIR}{name}', 'rb')
    tb.send_photo(message.from_user.id, photo)


edit_message = lambda markup, message_text, message: tb.edit_message_text(message_text,
                                                                          message.message.chat.id,
                                                                          message.message.message_id,
                                                                          reply_markup=markup)

get_edit_marcup = lambda message, message_text: MarkupFactory([[message.data.split(';')[-1]]],
                                                              callback=message_text).build()
