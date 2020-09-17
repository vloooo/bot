import os

from telebot import types

from calendar_utils import CalendarWithBlackDates
from const import tb, common_scripts, LUDA_ID, pm_map, current_date, next_year, PHOTO_DIR
from utils import send_photo, simple_callback
from db_actions import Session, Customer, Procedure, Order, get_or_create, Photo
from datetime import datetime
from callback import CallbackDataFactory


@tb.message_handler(commands=['start'])
def command_start(message):
    tb.send_message(message.from_user.id, "Добрый день, меня зовут Людмила Овсяникова. \n")
    send_photo('kote.jpg', message)
    tb.send_message(message.from_user.id, "я занимаюсь професиональным увеличением губ и прочим. \n"
                                          "с помощью данного бота вы можете ознакомиться с предоставляемвми услугами "
                                          "и записаться на продцедуру.\n"
                                          "мои работы вы можете посмотреть в истаграмме, \n"
                                          "тел. 9379992")
    simple_callback(common_scripts['get_contact'], message)


@tb.message_handler(content_types=['contact'])
def handle_contact(message):
    session = Session()
    get_or_create(session,
                  Customer,
                  id=message.from_user.id,
                  first_name=message.from_user.first_name,
                  last_name=message.from_user.last_name,
                  phone=message.contact.phone_number)
    session.close()

    simple_callback(common_scripts['choose_procedure'], message)


def handle_callback(message):
    data = CallbackDataFactory(message.data)
    for script in common_scripts.values():
        if script.prev_callback and script.prev_callback in data.last_item['key']:
            session = Session()
            customer = session.query(Customer).filter_by(id=message.from_user.id).first()
            setattr(customer, data.last_item['key'], data.last_item['value'])
            session.commit()
            session.close()

            simple_callback(script, message)
            break

    if "herpes" in message.data:
        session = Session()
        send_photo('kote.jpg', message)
        get_or_create(session,
                      Order,
                      customer_id=message.from_user.id,
                      procedure_id=session.query(Procedure).filter_by(command=data.data['type']).first().id)
        session.close()


    elif "pm_menu" in message.data:
        tb.send_message(message.from_user.id,
                        f"длинное описание продцедуры Перманентный макияж {message.data[3:]}: \n"
                        "для дальнейшего продолжения работы мне нужно задать вам пару вопросов",
                        reply_markup=types.ReplyKeyboardRemove())
        extra_callback = f"pm_{pm_map[data.data['pm_menu']]}"
        simple_callback(common_scripts['start_questions'], message, extra_callback=extra_callback)

    elif "call_in_hour" in message.data:
        tb.send_message(LUDA_ID, "позвонить клиенту tel. " + 'user.tel')

    elif "assign" in message.data:
        simple_callback(common_scripts['calendar'], message)

    elif "time" in message.data:
        session = Session()
        order = get_or_create(session, Order, customer_id=message.from_user.id)
        order.datetime = datetime.strptime(f"{data.data['date']} {data.data['time']}", '%Y-%m-%d %H:%M')
        session.commit()
        session.close()

        tb.send_message(message.from_user.id, f"я записала вас. {data.data['date']} {data.data['time']}")


@tb.message_handler(content_types=['photo', 'document'])
def handle_photo(message):
    session = Session()
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    else:
        file_id = message.document.file_id

    downloaded_file = tb.download_file(tb.get_file(file_id).file_path)
    customer = session.query(Customer).filter_by(id=message.from_user.id).first()

    customer_folder = f"{customer.id}_{customer.first_name}_{customer.last_name}/"
    photos_amount = len(customer.photos)
    photo_path = f"{PHOTO_DIR}{customer_folder}{photos_amount}.jpg"
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)

    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    session.add(Photo(customer_id=customer.id, path=photo_path))
    session.commit()

    # photos_amount = len(customer.photos)
    session.close()

    # if photos_amount < 3:
    #     tb.send_message(message.from_user.id, f"Пожалуйста, прешлите ещё {3-photos_amount} фото")
    # else:
    simple_callback(common_scripts['to_assign'], message)


@tb.callback_query_handler(func=CalendarWithBlackDates.func())
def handle_calendar(c):
    result, key, step = CalendarWithBlackDates(locale='ru',
                                               min_date=current_date,
                                               max_date=next_year).process(c.data)
    if not result and key:
        tb.edit_message_text("Выберите день",
                             c.message.chat.id,
                             c.message.message_id,
                             reply_markup=key)
    elif result:
        markup = CalendarWithBlackDates().build_time(result)
        tb.edit_message_text(f"Вы берите удобное для вас время {result}",
                             c.message.chat.id,
                             c.message.message_id,
                             reply_markup=markup)


@tb.callback_query_handler(func=handle_callback)
@tb.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Увеличение губ":
        simple_callback(common_scripts['push_lips_desc'], message)
        simple_callback(common_scripts['start_questions'], message, extra_callback='push_lips')

    elif message.text == 'Перманентный макияж':
        simple_callback(common_scripts['get_pm_type'], message)

    elif message.text == 'Ботекс':
        simple_callback(common_scripts['botex_desc'], message)
        simple_callback(common_scripts['start_questions'], message, extra_callback='botex')

    elif message.text == 'Мезотерапия головы':
        simple_callback(common_scripts['mezo_head_desc'], message)
        simple_callback(common_scripts['start_questions'], message, extra_callback='mezo_head')

    elif message.text == 'Выбор продцедуры':
        simple_callback(common_scripts['choose_procedure'], message)

    else:
        simple_callback(common_scripts['undetected'], message)


if __name__ == '__main__':
    tb.polling(none_stop=True, interval=0)
