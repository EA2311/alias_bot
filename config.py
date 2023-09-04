from dotenv import dotenv_values


def init():
    global token, answer, words, player, scoring

    token = dotenv_values(".env")['BOT_TOKEN']
    answer = ""  # правильна відповідь
    words = []  # список обраних слів
    player = ""  # ведучий гравець
    scoring = {}  # словник (нікнейм гравця: кількість балів)
