from calendar import monthrange
from datetime import datetime

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import WYearTelegramCalendar
from telegram_bot_calendar.base import *

from callback import CallbackDataFactory
from db_actions import Session, BlackDates, Order
from db_actions import get_or_create


class CalendarWithBlackDates(WYearTelegramCalendar):

    def _build_days(self, *args, **kwargs):
        session = Session()
        days_num = monthrange(self.current_date.year, self.current_date.month)[1]

        start = self.current_date.replace(day=1)
        days = self._get_period(DAY, start, days_num)
        for d in days:
            if d:
                options = self.get_buttons(d.strftime('%Y-%m-%d'))
                if options == 0:
                    get_or_create(BlackDates, date=d)
        black_days = [black_date.date for black_date in session.query(BlackDates).all()]
        session.close()

        valid_dates = [
            self._build_button(d.day if d and d.weekday() < 5 and d not in black_days else self.empty_day_button,
                               SELECT if d and d.weekday() < 5 and d not in black_days else NOTHING, DAY, d,
                               is_random=True)
            for d in days
        ]
        days_buttons = rows(
            valid_dates,
            self.size_day
        )

        days_of_week_buttons = [[
            self._build_button(self.days_of_week[self.locale][i], NOTHING) for i in range(7)
        ]]

        nav_buttons = self._build_nav_buttons(DAY, diff=relativedelta(months=1),
                                              maxd=max_date(start, MONTH),
                                              mind=min_date(start + relativedelta(days=days_num - 1), MONTH))

        self._keyboard = self._build_keyboard(days_of_week_buttons + days_buttons + nav_buttons)

    @staticmethod
    def get_row_width(count):
        if count < 5:
            return 5
        elif count == 6 or count == 9:
            return 3
        else:
            return 4

    @staticmethod
    def get_buttons(choosen_date):
        session = Session()
        btns = []
        orders = session.query(Order).all()
        busy_time = []
        for order in orders:
            for add_time in range(order.procedures.duration):
                if order.datetime is not None:
                    busy_time.append(order.datetime.replace(hour=order.datetime.hour+add_time))
        session.close()

        for i in range(8, 19):
            button_time = f"{str(i).rjust(2, '0')}:00"
            operated_time = datetime.strptime(f"{choosen_date} {button_time}", '%Y-%m-%d %H:%M')

            if operated_time not in busy_time:
                callback = CallbackDataFactory({'time': button_time, 'date': choosen_date})
                btn = InlineKeyboardButton(button_time, callback_data=callback.str)
                btns.append(btn)

        return btns

    def build_time(self, choosen_date):
        keyboard = InlineKeyboardMarkup()
        btns = self.get_buttons(choosen_date)
        keyboard.add(*btns, row_width=self.get_row_width(len(btns)))
        return keyboard
