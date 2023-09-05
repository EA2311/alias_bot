# Alias Telegram Bot

This project was created in September 2022 to gain hands-on skills in creating a Telegram bot using Python.
But now, in September 2023, it was added to git, modified, slightly refactored, and uploaded to this GitHub.
The main purpose of the bot is the ability to play a game in which one player explains a word, 
and the others have to guess it. And this process takes place directly in the Telegram chat.

---

## Technology stack

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![image](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
---

## Main features

In order to fully test the capabilities of the bot, it needs to be added to a group chat. It has the following commands:
- **/start**: responsible for starting a new game.
The bot sends a message asking the host player to choose a topic of words. After choosing a topic, the bot sends a 
message in which only the leading player can see the guessed word and will have the opportunity to replace it with the 
next word. The other players must guess the word using the lead player's hints. If one of the players (not the host) 
sends the correct word, the bot will report this and a new round will have to be started. The player who guesses 10 
words wins.

- **/joke**: after invoking this command, the bot will send a random thematic joke that will be retrieved from the link 
https://geek-jokes.sameerkumar.website/api?format=text (although this function is not related to the main game, it can be quite fun for a group of friends)

---

## Usage

### To try this project on your local machine follow the next steps:

1. Clone this repository on your local machine:
```bash
git clone https://github.com/EA2311/alias_bot.git
```
2. Navigate to the project directory:
```bash
cd alias_bot
```
3. Create the ".env" file with the next variable inside:
```
BOT_TOKEN = *Your telegram bot token here*
```
4. Create and activate the virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
5. Install dependencies:
```bash
pip install -r requirements.txt
```
6. Start the Alias Bot locally:
```bash
python bot.py
```

---

### Thank you for your interest in my project!
