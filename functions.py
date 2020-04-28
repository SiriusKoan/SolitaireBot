import sqlite3 as sql
import requests
import json
from random import randint
import string
from telebot import types

def get_random_word(start):
    r = requests.get('https://api.datamuse.com/words?sp=%s*&max=10'%start)
    if start in string.ascii_letters:
        if r.ok:
            result = []
            words = json.loads(r.text)
            if words == []:
                return 'lose'
            for word in words:
                result.append(word['word'])
            return result[randint(0, len(result) - 1)]
        else:
            return False
    return False

def make_inline_button(word):
    inline_button = types.InlineKeyboardMarkup()
    inline_button.add(types.InlineKeyboardButton('meaning', url = 'https://dictionary.cambridge.org/zht/dictionary/english/%s'%word))
    inline_button.add(types.InlineKeyboardButton('continue', switch_inline_query_current_chat = word[-1]))
    return inline_button

def get_history(chat_id):
    con = sql.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT id, rounds FROM games')
    history = cur.fetchall()
    con.close()
    if history:
        return history
    else:
        return False