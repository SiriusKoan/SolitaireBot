import telebot
from telebot import types
from functions import *
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['new'])
def receive_new_game_msg(message):
    pass