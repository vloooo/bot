import telebot
from telebot import types

tb = telebot.TeleBot('1393369006:AAGMXXQ01qwn3PqfwOfq9edp607Sah_xq6o')
LUDA_ID = ''

@tb.message_handler(commands=['start', 'help'])
def command_help(message):
    # markup = types.ReplyKeyboardMarkup(row_width=2)
    # itembtn1 = types.KeyboardButton('a')
    # itembtn2 = types.KeyboardButton('v')
    # itembtn3 = types.KeyboardButton('d')
    # markup.add(itembtn1, itembtn2, itembtn3)
    # tb.send_message(message.from_user.id, "Choose one letter:", reply_markup=markup)

    # or add KeyboardButton one row at a time:

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_contact = types.KeyboardButton("Oтправить контакт", request_contact=True)
    markup2.row(get_contact)

    # markup.row(photos)
    # markup.row(assign)

    photo = open('C:\\Users\\vladm\\PycharmProjects\\ludmila_pigmenta_bot\\photos\\kote.jpg', 'rb')
    tb.send_message(message.from_user.id, "Добрый день, меня зовут Людмила Овсяникова. \n")
    tb.send_photo(message.from_user.id, photo)
    tb.send_message(message.from_user.id, "я занимаюсь професиональным увеличением губ и прочим. \n"
                                          "с помощью данного бота вы можете ознакомиться с предоставляемвми услугами и записаться на продцедуру.\n"
                                          "мои работы вы можете посмотреть в истаграмме, \n"
                                          "тел. 9379992")
    tb.send_message(message.from_user.id, "пожалуйста, отправьте ваш контакт", reply_markup=markup2)

    # tb.reply_to(message, "Hello, did someone call for help?")


@tb.message_handler(content_types=['contact'])
def handle_contact(message):
    print(message.contact)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    p_m = types.KeyboardButton('Перманентный макияж')
    push_lips = types.KeyboardButton('Увеличение губ')
    mezo_therapy = types.KeyboardButton('Мезотерапия головы')
    botex = types.KeyboardButton('Ботекс')
    assign = types.KeyboardButton('Хочу записаться на продцедуру')
    photos = types.KeyboardButton('Фото работ')
    markup.row(push_lips, p_m)
    markup.row(botex, mezo_therapy)
    tb.send_message(message.from_user.id, "Выбирите продцедуру:", reply_markup=markup)


def handle_callback(message):
    print(message)
    if message.data == "lips_yes" or message.data == "lips_no":
        print("zapisal")
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton('da', callback_data='ledocoin_yes')
        no = types.InlineKeyboardButton('net', callback_data='ledocoin_no')
        markup.row(yes, no)

        tb.send_message(message.from_user.id, "у вас есть алергия на ледокоин?", reply_markup=markup)

    if "ledocoin" in message.data:
        print("zapisal")
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton('often', callback_data='herpes_yes')
        no = types.InlineKeyboardButton('rarely', callback_data='herpes_no')
        markup.row(yes, no)

        tb.send_message(message.from_user.id, "часто ли высыпает герпес на губах?", reply_markup=markup)

    if "herpes" in message.data:
        tb.send_message(message.from_user.id, "для дальнейшей работы, я бы хотела получить фото ваших губ в 3-х ракурсах. пример фотографий ниже")
        photo = open('C:\\Users\\vladm\\PycharmProjects\\ludmila_pigmenta_bot\\photos\\kote.jpg', 'rb')
        tb.send_photo(message.from_user.id, photo)

    if "call_in_hour" in message.data:
        tb.send_message(LUDA_ID, "позвонить клиенту tel. " + 'user.tel')

    if "assign" in message.data:
        tb.send_message(message.from_user.id, "выберите дату для записи")


@tb.message_handler(content_types=['photo'])
def handle_contact(message):
    print('polozil_BD')
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton('связаться в течение часа', callback_data='call_in_hour')
    no = types.InlineKeyboardButton('записаться', callback_data='assign')
    markup.row(yes, no)
    tb.send_message(message.from_user.id,
                    "ниже представлены цены за процедуру в зависимосте от препарата. \n"
                    "цены ..........", reply_markup=markup)


@tb.callback_query_handler(func=handle_callback)
@tb.message_handler(content_types=['text', 'update'])
def handle_contact(message):
    print(message)
    if message.text == "Увеличение губ":
        markup = types.InlineKeyboardMarkup()
        markup2 = types.ReplyKeyboardMarkup()
        yes = types.InlineKeyboardButton('da', callback_data='lips_yes')
        no = types.InlineKeyboardButton('net', callback_data='lips_no')
        call = types.InlineKeyboardButton('заказать звонок для консультации специалиста', callback_data='callback')
        markup.row(yes, no)
        markup2.row(call)

        tb.send_message(message.from_user.id, "длинное описание продцедуры увеличения губ: \n"
                                              "для дальнейшего продолжения работы мне нужно задать вам пару вопросов")
        tb.send_message(message.from_user.id, "увеличевали ли вы убы ранее?", reply_markup=markup)
        # tb.send_message(message.from_user.id, "", reply_markup=markup2)


        # tb.send_poll(message.from_user.id,
        #              question="выберите препарат",
        #              options=[
        #                  "препарат1",
        #                  "препарат2",
        #                  "препарат3",
        #                  "препарат4",
        #              ])
    else:
        tb.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


tb.polling(none_stop=True, interval=0)
