import requests

import telebot
from dotenv import dotenv_values

from services import add_buttons, start_new_round

config = dotenv_values(".env")

bot = telebot.TeleBot(config["BOT_TOKEN"])

answer = ""  # правильна відповідь
words = []  # список обраних слів
player = ""  # ведучий гравець
scoring = {}  # словник (нікнейм гравця: кількість балів)




@bot.message_handler(commands=['joke'])
def joke(message):
    url = 'https://geek-jokes.sameerkumar.website/api?format=text'
    response = requests.get(url).text.strip('"')

    from deep_translator import MyMemoryTranslator
    translated = MyMemoryTranslator(source="en-US", target="uk-UA").translate(text=response)

    bot.send_message(message.chat.id, text=translated)


@bot.message_handler(commands=['start'])
def start(message):
    global player
    player = message.from_user.username
    bot.send_message(
        message.chat.id,
        text=f'Привіт {message.from_user.first_name}! Обери тему для гри 🎮',
        reply_markup=add_buttons('categories')
    )


@bot.callback_query_handler(func=lambda call: True)
def check_inline_keyboard(call):
    global answer, words, player

    if call.data == 'animals':
        start_new_round(call, bot, 'animals')
    elif call.data == 'technical':
        start_new_round(call, bot, 'technical')
    elif call.data == 'show':
        if call.from_user.username == player:
            bot.answer_callback_query(call.id, text=answer, show_alert=True)
        else:
            bot.answer_callback_query(call.id, text='Неможна ❌', show_alert=True)
    elif call.data == 'next':
        if call.from_user.username == player:
            answer = words.pop()
        else:
            bot.answer_callback_query(call.id, text='Не твоя черга!', show_alert=True)
    elif call.data == 'new_round':
        start_new_round(call, bot)


@bot.message_handler(content_types=['text'])
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
                bot.send_message(chat_id, text=f'Гравець {current_user} переміг 🎀')
            else:
                bot.send_message(chat_id, text=f'Ти відгадав! У {current_user} {current_user_score} балів',
                                 reply_markup=add_buttons('new_round'))
        else:
            scoring[current_user] = 1
            bot.send_message(chat_id, text=f'Ти відгадав! У {current_user} {scoring[current_user]} балів',
                             reply_markup=add_buttons('new_round'))


bot.polling(none_stop=True)
