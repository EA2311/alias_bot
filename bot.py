import requests

import telebot

from services import add_buttons, start_new_round
import config


config.init()

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['joke'])
def joke(message):
    url = 'https://geek-jokes.sameerkumar.website/api?format=text'
    response = requests.get(url).text.strip('"')

    from deep_translator import MyMemoryTranslator
    translated = MyMemoryTranslator(source="en-US", target="uk-UA").translate(text=response)

    bot.send_message(message.chat.id, text=translated)


@bot.message_handler(commands=['start'])
def start(message):
    config.player = message.from_user.username
    bot.send_message(
        message.chat.id,
        text=f'Привіт {message.from_user.first_name}! Обери тему для гри 🎮',
        reply_markup=add_buttons('categories')
    )


@bot.callback_query_handler(func=lambda call: True)
def check_inline_keyboard(call):
    if call.data == 'animals':
        start_new_round(call, bot, 'animals')
    elif call.data == 'technicals':
        start_new_round(call, bot, 'technicals')
    elif call.data == 'show':
        if call.from_user.username == config.player:
            bot.answer_callback_query(call.id, text=config.answer, show_alert=True)
        else:
            bot.answer_callback_query(call.id, text='Неможна ❌', show_alert=True)
    elif call.data == 'next':
        if call.from_user.username == config.player:
            config.answer = config.words.pop()
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
    current_user = message.from_user.username
    chat_id = message.chat.id

    if message.text.lower() == config.answer.lower() and config.player != current_user:
        if current_user in config.scoring.keys():  # якщо нік гравця є в словнику scoring
            config.scoring[current_user] += 1
            current_user_score = config.scoring[current_user]
            if current_user_score == 10:
                bot.send_message(chat_id, text=f'Гравець {current_user} переміг 🎀')
            else:
                bot.send_message(chat_id, text=f'Ти відгадав! У {current_user} {current_user_score} балів',
                                 reply_markup=add_buttons('new_round'))
        else:
            config.scoring[current_user] = 1
            bot.send_message(chat_id, text=f'Ти відгадав! У {current_user} {config.scoring[current_user]} балів',
                             reply_markup=add_buttons('new_round'))


bot.polling(none_stop=True)
