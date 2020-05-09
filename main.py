import telebot
from telebot import types
from functions import *
import config
from game import Game
from random import randint
from Error import *

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def receive_start(message):
    bot.send_message(message.chat.id, 'Start.')

@bot.message_handler(commands = ['new'])
def receive_new_game_msg(message):
    chat_id = message.chat.id
    if chat_id in games:
        bot.send_message(chat_id, 'A game has created.')
    else:
        games[chat_id] = Game(chat_id, get_random_word(chr(randint(97, 122))), message.from_user.username)
        bot.send_message(chat_id, 'Start a new game!\nCreater: @%s'%message.from_user.username)

@bot.message_handler(commands = ['kill', 'delete'])
def receive_kill_game(message):
    chat_id = message.chat.id
    if chat_id in games:
        del games[chat_id]
        bot.send_message(chat_id, 'Kill current game.')
    else:
        bot.send_message(chat_id, 'There is not any game currently.')

@bot.message_handler(commands = ['status'])
def receive_game_status(message):
    chat_id = message.chat.id
    if chat_id in games:
        status = games[chat_id].get_status()
        bot.send_message(chat_id, 'Game Status: %s\nCurrent Player: @%s\nWord: %s\nRounds: %s'%(status[0], status[1], status[2], status[3]))
    else:
        bot.send_message(chat_id, 'You have to start a game first.')

@bot.message_handler(commands = ['join'])
def receive_join_msg(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if chat_id in games:
        players = games[chat_id].get_all_players()
        if username not in players:
            bot.send_message(chat_id, '*@%s* join the game!'%username, parse_mode = 'Markdown')
            games[chat_id].join(username)
    else:
        bot.send_message(chat_id, 'You have to create a game first.')

@bot.message_handler(commands = ['start_game'])
def receive_start_game(message):
    chat_id = message.chat.id
    if chat_id in games and games[chat_id].get_status()[0] != 'running':
        word = games[chat_id].get_current_word()
        games[chat_id].start()
        inline_button = make_inline_button(word)
        bot.send_message(chat_id, 'Game start!\nThe first word: *%s*'%word, parse_mode = 'Markdown', reply_markup = inline_button)
        bot.send_message(chat_id, 'The first player: @%s'%games[chat_id].get_current_player())
    else:
        bot.send_message(chat_id, 'You have to create a game first or end the current game.')

@bot.message_handler(commands = ['end_game'])
def receive_end_game(message):
    chat_id = message.chat.id
    if chat_id in games:
        bot.send_message(chat_id, 'Game end!\nTotal Rounds: %s'%str(games[chat_id].get_current_rounds()))
        games[chat_id].save_game()
        del games[chat_id]
    else:
        bot.send_message(chat_id, 'There is no game now.')

@bot.message_handler(commands = ['history'])
def receive_get_history(message):
    chat_id = message.chat.id
    history = get_history(chat_id)
    if history:
        msg = ''
        for i in history:
            msg += 'ID: %s Rounds: %s\n'%(i[0], i[1])
        bot.send_message(chat_id, msg)

@bot.inline_handler(lambda query: query.query != '')
def solitaire(query):
    username = query.from_user.username
    user_chat_id = query.from_user.id
    try:
        # check whether user in any group, but can't play personal mode
        chat_id = in_group(username, user_chat_id, games)
        if not chat_id:
            raise NotJoinGame


        if chat_id in games:
            if query.from_user.username == games[chat_id].get_current_player():
                start_with = games[chat_id].get_current_word()[-1]
                if query.query[0] == start_with:
                    inline_button = make_inline_button(query.query)
                    response = [types.InlineQueryResultArticle(0, query.query, types.InputTextMessageContent(query.query), reply_markup = inline_button)]
                    bot.answer_inline_query(query.id, response, cache_time = 1)
                else:
                    raise StartWithError(start_with)
            else:
                raise NotCurrentPlayerError
        else:
            print(games, chat_id)
            raise NotStartGameError
    except Exception as error:
        response = [types.InlineQueryResultArticle(0, str(error), types.InputTextMessageContent('illegal action'))]
        bot.answer_inline_query(query.id, response, cache_time = 1)

@bot.message_handler(func = lambda message: True)
def receive_word(message):
    chat_id = message.chat.id
    if 'inline_keyboard' in str(message):
        games[chat_id].pass_round(message.text)
        bot.reply_to(message, '@' + games[chat_id].get_current_player())

if __name__ == '__main__':
    games = dict()
    bot.polling()