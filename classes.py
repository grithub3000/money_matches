class Game:
    players = []
    money_on_table = 5
    history = []

    @classmethod
    def update_histories(cls):
        for player in cls.history[-1][:-1]:
            if player.status == "w":
                player.history.append(cls.money_on_table)
            elif player.status == "l":
                player.history.append(-cls.money_on_table)
        
    @classmethod
    def reset_statuses(cls):
        for player in cls.players:
            player.status = None

class Player:
    def __init__(self, name, money=0, wins=0, losses=0, history=None):
        self.name = name
        self.money = money
        self.status = None
        self.wins = wins
        self.losses = losses
        self.history = history if history is not None else []
    
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

def save_data():
    with open("save_file.py", "w") as output:
        print("from classes import Game, Player", file=output)
        for player in Game.players:
            print(f"Game.players.append(Player('{player.name}', {player.money}, " 
                  f"{player.wins}, {player.losses}, {player.history}))", file=output)
        

