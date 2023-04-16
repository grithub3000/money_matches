class Game:
    players = []
    money_on_table = 5
    history = []

    @classmethod
    def update_histories(cls):
        for player in cls.history[-1][:-1]:
            if player.status == "w":
                player.history.append(cls.money_on_table)
            else:
                player.history.append(-cls.money_on_table)
        
    @classmethod
    def reset_statuses(cls):
        for player in cls.players:
            player.status = None

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.status = None
        self.wins = 0
        self.losses = 0
        self.history = []
    
    def display_history(self):
        history_string = ""
        games = [game for game in Game.history if self in game]
        for i, game in enumerate(games, start=1):
            players = game[:-1]
            winners = players[:len(players)//2]
            losers = players[len(players)//2:]

            history_string += str(i) + ". "

            for player in winners:
                if player != winners[-1]:
                    history_string += player.name + ", "
                elif player != winners[0]:
                    history_string += "and " + player.name + " "
                elif player == winners[0]:
                    history_string += player.name + " "

            history_string += "beat "

            for player in losers:
                if player != losers[-1]:
                    history_string += player.name + ", "
                elif player != losers[0]:
                    history_string += "and " + player.name + " "
                elif player == losers[0]:
                    history_string += player.name + " "
            
            history_string += f"for ${game[-1]}\n"
        return history_string
    
    def __str__(self):
        return f"{self.name}: ${self.money}\n{self.wins}-{self.losses}"