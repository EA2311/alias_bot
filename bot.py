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


@bot.message_handler(commands=["start"])
def start(message):
    global player

    markup_inline = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(text="тварини", callback_data="animals")
    btn2 = types.InlineKeyboardButton(text="професії", callback_data="technical")

    markup_inline.add(btn1)
    markup_inline.add(btn2)

    player = message.from_user.username
    bot.send_message(
        message.chat.id,
        text=f"Привіт {message.from_user.first_name} обери тему для гри 🎮",
        reply_markup=markup_inline
    )


@bot.callback_query_handler(func=lambda call: True)
def сheck_inline_keyboard(call):
    global answer, words, player

    if call.data == "show":
        if call.from_user.username == player:
            bot.answer_callback_query(call.id, text=answer, show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="неможна ❌", show_alert=True)
    elif call.data == "next":
        if call.from_user.username == player:
            answer = words.pop()
        else:
            bot.answer_callback_query(call.id, text='Не твоя черга!', show_alert=True)
    elif call.data == "animals":
        markup_inline = types.InlineKeyboardMarkup()
        reset_words("animals")
        answer = words.pop()

        show_button = types.InlineKeyboardButton(text="подивитись слово 👀", callback_data="show")
        next_button = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        markup_inline.add(show_button)
        markup_inline.add(next_button)
        player = call.from_user.username
        bot.send_message(call.message.chat.id, text=f"Зараз пояснює слово {call.from_user.first_name} 🧠",
                         reply_markup=markup_inline)
    elif call.data == "technical":
        markup_inline = types.InlineKeyboardMarkup()
        reset_words("technical")
        answer = words.pop()

        show_button = types.InlineKeyboardButton(text="подивитись слово 👀", callback_data="show")
        next_button = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")

        markup_inline.add(show_button)
        markup_inline.add(next_button)
        player = call.from_user.username
        bot.send_message(call.message.chat.id, text=f"Зараз пояснює слово  {call.from_user.first_name}  🧠",
                         reply_markup=markup_inline)


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
        markup_inline = types.InlineKeyboardMarkup()

        if current_user in scoring.keys():  # якщо нік гравця є в словнику scoring
            current_user_score = scoring[current_user] + 1

            if current_user_score == 10:
                bot.send_message(chat_id, text=f"гравець {current_user} переміг 🎀", reply_markup=markup_inline)
            else:
                next_button = types.InlineKeyboardButton(text="наступне слово 🔜", callback_data="next")
                markup_inline.add(next_button)
                bot.send_message(chat_id, text=f"ти відгадав, у {current_user} {current_user_score} балів",
                                 reply_markup=markup_inline)
        else:
            scoring[current_user] = 1


bot.polling(none_stop=True)
