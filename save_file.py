from classes import Game, Player
Game.players.append(Player('Bob', 10, 2, 0, [5, 5]))
Game.players.append(Player('Joe', -10, 0, 2, [-5, -5]))
Game.history = [('Bob', 'Joe', 5), ('Bob', 'Joe', 5)]
