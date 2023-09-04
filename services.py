import random

from telebot import types


def _reset_words(file_name):
    """
    Read the file and put all words into the list. Then shuffle it.
    :param file_name: name of a txt file to read
    :return:
    """
    global words

    f = open(f"{file_name}.txt", "r", encoding="UTF-8")
    words = f.read().split("\n")
    f.close()
    random.shuffle(words)


def add_buttons(button_type='both'):
    """
    Create markup_inline with certain buttons inside.
    :param button_type:
    :return: InlineKeyboardMarkup with some InlineKeyboardButton.
    """
    markup_inline = types.InlineKeyboardMarkup()
    show_button = types.InlineKeyboardButton(text='Моє слово 👀', callback_data='show')
    next_button = types.InlineKeyboardButton(text='Оновити слово 🔜', callback_data='next')
    animals_button = types.InlineKeyboardButton(text='Тварини', callback_data='animals')
    technicals_button = types.InlineKeyboardButton(text='Професії', callback_data='technical')
    new_round_button = types.InlineKeyboardButton(text='Наступний раунд 🔜', callback_data='new_round')

    if button_type == 'show':
        return markup_inline.add(show_button)
    elif button_type == 'next':
        return markup_inline.add(next_button)
    elif button_type == 'categories':
        return markup_inline.add(animals_button, technicals_button)
    elif button_type == 'new_round':
        return markup_inline.add(new_round_button)
    else:
        return markup_inline.add(show_button, next_button)


def start_new_round(call, bot, category=None):
    """
    Get a new word for a player that will explain it and send a message with that player's username.

    :param category: specifies which word category will be reset to start a new game, optional
    :param call:
    """
    global answer, words, player

    if category:
        _reset_words(category)
    answer = words.pop()
    player = call.from_user.username
    bot.send_message(call.message.chat.id, text=f'Зараз пояснює слово {call.from_user.first_name} 🧠',
                     reply_markup=add_buttons())
