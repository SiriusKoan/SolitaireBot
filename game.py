import sqlite3 as sql
class Game:
    def __init__(self, chat_id, word, player):
        self.chat_id = chat_id
        self.word = word
        self.players = [player]
        self.current_player = player
        self.status = 'prepare'
        self.rounds = 0

    def join(self, new_player):
        if self.status == 'prepare':
            self.players.append(new_player)
            return True
        else:
            return False

    def get_status(self):
        return (self.status, self.current_player, self.word, self.rounds)

    def get_all_players(self):
        return self.players

    def get_current_player(self):
        return self.current_player

    def get_current_word(self):
        return self.word
    
    def get_current_rounds(self):
        return self.rounds

    def start(self):
        self.status = 'running'
        self.rounds += 1
        return self.word

    def pass_round(self, word):
        self.rounds += 1
        try:
            self.current_player = self.players[self.players.index(self.current_player)]
        except IndexError:
            # to the last player, so next is the first player
            self.current_player = self.players[0]
        self.word = word

    def save_game(self):
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute('INSERT INTO games (chat_id, rounds) VALUES (?, ?)', (self.chat_id, self.rounds))
        con.commit()
        con.close()