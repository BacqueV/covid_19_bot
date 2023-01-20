from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_back = InlineKeyboardButton(text='Back', callback_data='back')
btn_next = InlineKeyboardButton(text='Next', callback_data='next')

markup_start = InlineKeyboardMarkup().row(btn_next)
markup_middle = InlineKeyboardMarkup().row(btn_back, btn_next)
markup_end = InlineKeyboardMarkup().row(btn_back)
