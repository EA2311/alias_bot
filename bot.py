import telebot
from telebot import types
import random
from dotenv import dotenv_values

config = dotenv_values(".env")

bot = telebot.TeleBot(config["BOT_TOKEN"])

answer = ""  # правильна відповідь
words = []  # список обраниз слів
player = ""  # ведучий гравець
scoring = {}  # словник (нікнейм гравця: кількість балів)


# зчитує слова за файлу та перемішує їх
def reset_words(fname):
    global words

    f = open(f"{fname}.txt", "r", encoding="UTF-8")
    words = f.read().split("\n")
    f.close()
    random.shuffle(words)  # перемішує список слів


def add_buttons(button_type='both'):
    """
    Create markup_inline with certain buttons inside.
    :param button_type:
    :return: InlineKeyboardMarkup with some InlineKeyboardButton.
    """
    markup_inline = types.InlineKeyboardMarkup()
    show_button = types.InlineKeyboardButton(text='подивитись слово 👀', callback_data='show')
    next_button = types.InlineKeyboardButton(text='наступне слово 🔜', callback_data='next')
    animals_button = types.InlineKeyboardButton(text='тварини', callback_data="animals")
    technicals_button = types.InlineKeyboardButton(text='професії', callback_data="technical")
    new_round_button = types.InlineKeyboardButton(text='наступний раунд 🔜', callback_data='new_round')

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


def start_new_round(call, category=None):
    """
    Get a new word for a player that will explain it and send a message with that player's username.

    :param category: specifies which word category will be reset to start a new game, optional
    :param call:
    """
    global answer, words, player

    if category:
        reset_words(category)
    answer = words.pop()
    player = call.from_user.username
    bot.send_message(call.message.chat.id, text=f'Зараз пояснює слово {call.from_user.first_name} 🧠',
                     reply_markup=add_buttons())


@bot.message_handler(commands=["start"])
def start(message):
    global player
    player = message.from_user.username
    bot.send_message(
        message.chat.id,
        text=f'Привіт {message.from_user.first_name} обери тему для гри 🎮',
        reply_markup=add_buttons('categories')
    )


@bot.callback_query_handler(func=lambda call: True)
def check_inline_keyboard(call):
    global answer, words, player

    if call.data == 'animals':
        start_new_round(call, 'animals')
    elif call.data == 'technical':
        start_new_round(call, 'technical')
    elif call.data == 'show':
        if call.from_user.username == player:
            bot.answer_callback_query(call.id, text=answer, show_alert=True)
        else:
            bot.answer_callback_query(call.id, text='неможна ❌', show_alert=True)
    elif call.data == 'next':
        if call.from_user.username == player:
            answer = words.pop()
        else:
            bot.answer_callback_query(call.id, text='Не твоя черга!', show_alert=True)
    elif call.data == 'new_round':
        start_new_round(call)


@bot.message_handler(content_types=["text"])
def check_word(message):
    """
    Checks whether the word is equal to the correct answer and adds a point to the user who guessed the word.
    If the player who guessed the last word scores 10 points, he wins and the game ends.
    """
    global scoring
    current_user = message.from_user.username
    chat_id = message.chat.id

    if message.text.lower() == answer.lower() and player != current_user:
        if current_user in scoring.keys():  # якщо нік гравця є в словнику scoring
            scoring[current_user] += 1
            current_user_score = scoring[current_user]
            if current_user_score == 10:
                bot.send_message(chat_id, text=f'гравець {current_user} переміг 🎀')
            else:
                bot.send_message(chat_id, text=f'ти відгадав, у {current_user} {current_user_score} балів',
                                 reply_markup=add_buttons('new_round'))
        else:
            scoring[current_user] = 1
            bot.send_message(chat_id, text=f'ти відгадав, у {current_user} {scoring[current_user]} балів',
                             reply_markup=add_buttons('new_round'))


bot.polling(none_stop=True)
