from datetime import date

import telebot
from telebot.types import ReplyKeyboardRemove

from calendar_utils import CalendarWithBlackDates

current_date = date.today()
next_year = current_date.replace(year=current_date.year + 1)


class Answers:
    def __init__(self,
                 prev_question=None,
                 prev_callback=None,
                 question=None,
                 callback=None,
                 rows=None,
                 markup=None):
        self.prev_question = prev_question
        self.prev_callback = prev_callback
        self.question = question
        self.callback = callback
        self.rows = rows
        self.markup = markup


tb = telebot.TeleBot('1393369006:AAGMXXQ01qwn3PqfwOfq9edp607Sah_xq6o')
LUDA_ID = ''
PHOTO_DIR = '/home/NIX/ovsianikov/projects/bot/photos/'
pm_map = {'брови': 'eyebrow', 'губы': 'lips', 'ресницы': 'eyelash'}

common_scripts = {'new_lips': Answers(
    prev_question="увеличевали ли вы убы ранее?",
    prev_callback='previously',
    question="у вас есть алергия на ледокоин?",
    callback='ledocain',
    rows=[['да', 'нет']]
),
    'ledocain': Answers(
        prev_question="у вас есть алергия на ледокоин?",
        prev_callback='ledocain',
        question="часто ли высыпает герпес на губах?",
        callback='herpes',
        rows=[['часто', 'не часто', 'небывает']]
    ),
    'herpes': Answers(
        prev_question="часто ли высыпает герпес на губах?",
        prev_callback='herpes',
        question="для дальнейшей работы, я бы хотела получить фото вашего лица. "
                 "пример фотографий ниже"
    ),
    'choose_procedure': Answers(
        question="Выбирите продцедуру:",
        rows=[['Перманентный макияж', 'Увеличение губ'],
              ['Мезотерапия головы', 'Ботекс']]
    ),
    'to_assign': Answers(
        question="ниже представлены цены за процедуру в зависимосте от препарата. \n"
                 "цены ..........",
        callback='assign',
        rows=[['связаться в течение часа', 'записаться']]
    ),
    'undetected': Answers(
        question="Вы можете ознакомиться с предоставляемыми услугами",
        rows=[['Выбор продцедуры']]
    ),
    'get_contact': Answers(
        question="пожалуйста, отправьте ваш контакт",
        rows=[["Oтправить контакт"]]
    ),
    'calendar': Answers(
        question="выберите дату для записи",
        markup=CalendarWithBlackDates(min_date=current_date,
                                      max_date=next_year,
                                      locale='ru').build()[0]
    ),
    'start_questions': Answers(
        question="увеличевали ли вы убы ранее?",
        callback='previously',
        rows=[['да', 'нет']]
    ),
    'mezo_head_desc': Answers(
        question="длинное описание продцедуры Мезотерапия головы: \n"
                 "для дальнейшего продолжения работы мне нужно задать вам пару вопросов",
        markup=ReplyKeyboardRemove()
    ),
    'push_lips_desc': Answers(
        question="длинное описание продцедуры увеличения губ: \n"
                 "для дальнейшего продолжения работы мне нужно задать вам пару вопросов",
        markup=ReplyKeyboardRemove()
    ),
    'botex_desc': Answers(
        question="длинное описание продцедуры Ботекс: \n"
                 "для дальнейшего продолжения работы мне нужно задать вам пару вопросов",
        markup=ReplyKeyboardRemove()
    ),
    'get_pm_type': Answers(
        question="выберите область для макияжа.",
        callback='pm_menu',
        rows=[['брови', 'губы', 'ресницы']]
    ),
}
