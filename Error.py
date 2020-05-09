class StartWithError(Exception):
    def __init__(self, should_start_with):
        self.start_with = should_start_with
    def __str__(self):
        return 'The word has to start with "%s"'%self.start_with

class NotCurrentPlayerError(Exception):
    def __str__(self):
        return 'You are not the current player.'

class NotStartGameError(Exception):
    def __str__(self):
        return 'You have to start a game first.'

class NotJoinGame(Exception):
    def __str__(self):
        return 'You have not join game.'