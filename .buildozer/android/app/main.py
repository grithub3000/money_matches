from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from classes import *
from kivy.uix.togglebutton import ToggleButton
import save_file as save_file

class MoneyMatch(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.6)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        buttons = GridLayout()
        buttons.cols = 2
        
        if not Game.players:
            return self.add_names()
        
        self.window.add_widget(Label(text="Automatically saved data was found from your"
                                    " last time\nrunning the program.\nWould you like to"
                                    " load this data?",
                                    font_size=40))
        
        self.window.add_widget(buttons)
        buttons.add_widget(Button(text="Yes",
                                  background_color="#00FFCE",
                                  font_size=40,
                                  on_release=lambda x: self.play()
                                  ))
        
        buttons.add_widget(Button(text="No\n(Delete saved file)",
                                  background_color="#00FFCE",
                                  font_size=40,
                                  on_release=self.clear_file
                                  ))
        
        return self.window
    
    def clear_file(self, instance):
        with open("save_file.py", "w") as output:
            print("", file=output)
        Game.players.clear()
        Game.history.clear()
        return self.add_names()
        
    def add_names(self):
        self.window.clear_widgets()

        self.window.add_widget(Label(
                                text="Add player names, each seperated by a comma",
                                font_size=40,
                                color="#00FFCE"
                                ))
         
        #Player name inputs
        self.input = (TextInput(
                      multiline=True,
                      padding_y = (10, 10),
                      size_hint=(1, 0.5)
                      ))
        self.window.add_widget(self.input)
        
        #Continue Button
        self.button = Button(
                      text="Continue",
                      on_release=self.check_names,
                      size_hint=(1, 0.5), 
                      bold=True,
                      background_color="#00FFCE"
                      )
        self.window.add_widget(self.button)
        
        #self.window.add_widget(Image(source="money.webp"))

        #Error Button
        self.error = Label(
                     text="",
                     color="red",
                     size_hint_y=0.1
                     )
        
        self.window.add_widget(self.error)

        return self.window
    
    def check_names(self, instance):
        names = [player.name for player in Game.players]
        if "," in self.input.text:
            names += [name.strip().title() for name in self.input.text.split(",")]
        elif len(Game.players) == 0:
            return self.name_error()
        
        #If Game.players already has players, and you are just adding 1 more player
        else:
            names.append(self.input.text.title().strip())

        for name in names:
            if names.count(name) > 1 or not 2 <= len(name) <= 7:
                return self.name_error()
        
        for name in names:
            if name not in [player.name for player in Game.players]:
                Game.players.append(Player(name))
        self.play()

    def name_error(self):
        self.error.text="\nEach name must be unique and\nbetween 2 and 7 characters long"    

    def play(self):
        Game.reset_statuses()
        save_data()
        #Display Player Money
        
        self.window.clear_widgets()
        self.window.size_hint_x = 0.8
        self.window.size_hint_y = 0.8
        self.window.cols = 1
        self.top3cols = GridLayout()
        self.top3cols.cols = 3
        self.top3cols.size_hint_y = 6
        self.window.add_widget(self.top3cols)

        def status_lambda(i, status):
            if status == "w":
                return lambda x: self.mark_winner(Game.players[i])
            elif status == "l":
                return lambda x: self.mark_loser(Game.players[i])
        
        def history_lambda(i):
            return lambda x: self.show_history(Game.players[i])
        
        for i, player in enumerate(Game.players):
            self.top3cols.add_widget(Button(
                                    text=f"{player}",
                                    font_size=40,
                                    on_release=history_lambda(i),
                                    background_color="#00FFCE"
                                    ))
            toggle_button_w = ToggleButton(
                                         group=f"{player}-w/l",
                                         text="Winner",
                                         on_press=status_lambda(i, "w")
                                        )
            toggle_button_l = ToggleButton(
                                         group=f"{player}-w/l",
                                         text="Loser",
                                         on_press=status_lambda(i, "l")
                                        )
            self.top3cols.add_widget(toggle_button_w)
            self.top3cols.add_widget(toggle_button_l)
        
        
        #Money on table
        self.bottom3cols = GridLayout()
        self.bottom3cols.cols = 3
        self.bottom3cols.size_hint_y=2
        
        
        money_choices = [5, 10, 15, 25, 50, 100]
        
        def make_lambda(i):
            return lambda x: self.set_money(money_choices[i])
        
        self.window.add_widget(Label(
                                text=f"Money match for:",
                                font_size=40
                                ))
        
        self.window.add_widget(self.bottom3cols)
        
        for i, number in enumerate(money_choices):
            money_toggle = ToggleButton(
                                        text=f"${number}",
                                        group="money",
                                        on_press=make_lambda(i))
            self.bottom3cols.add_widget(money_toggle)
            if money_choices[i] == Game.money_on_table:
                money_toggle.state="down"
        
        self.window.add_widget(Button(
                                text="Update",
                                on_release=self.update_money,
                                background_color="#00FFCE"
                                ))
        
        self.window.add_widget(Button(
                                      text="Undo",
                                      on_release=self.undo,
                                      background_color="#00FFCE"
                                      ))
        
        self.window.add_widget(Button(
                                      text="Add Players",
                                      on_release=lambda x: self.add_names(),
                                      background_color="#00FFCE"
                                      ))
        
        self.uneven_error = Label(
                                  text="",
                                  color="red",
                                 )

        self.window.add_widget(self.uneven_error)
                                
    def show_history(self, player):
        self.window.clear_widgets()
        #Player's label
        self.window.add_widget(Label(
                                    text=f"{player}",
                                     font_size=32,
                                    ))
        #Player's history
        self.window.add_widget(Label(text=f"{player.display_history()}"))

        #Back Button
        self.window.add_widget(Button(
                                      text="Return", 
                                      on_release=lambda x: self.play(),
                                      background_color="#00FFCE",
                                      size_hint_y=0.25
                                      ))

    def set_money(self, money):
        Game.money_on_table = money
    
    def mark_winner(self, player):
        if player.status == "w":
            player.status = None
        else:
            player.status = "w"
        
    def mark_loser(self, player):
        if player.status == "l":
            player.status = None
        else:
            player.status = "l"
        
    def update_money(self, instance):
        winners = [player.name for player in Game.players if player.status == "w"]
        losers = [player.name for player in Game.players if player.status == "l"]

        if len(winners) == 0:
            return self.show_error()

        if len(losers) == 0 and len(winners) == len(Game.players) / 2:
            losers = [player.name for player in Game.players if player.name not in winners]
            for name in losers:
                player = search_by_name(name)
                player.status = "l"

        if len(winners) != len(losers):
            return self.show_error()
        
        #If teams are even:
        for name in winners:
            player = search_by_name(name)
            player.money += Game.money_on_table
            player.wins += 1
        for name in losers:
            player = search_by_name(name)
            player.money -= Game.money_on_table
            player.losses += 1
        Game.history.append(tuple(winners + losers + [Game.money_on_table]))
        
        Game.update_histories()
        Game.reset_statuses()
        save_data()
        return self.play()
    
    def show_error(self):
        self.uneven_error.text="ERROR:\nUneven or empty Teams"
    
    def undo(self, instance):
        if len(Game.history) == 0:
            return
        for name in Game.history.pop()[:-1]:
            player = search_by_name(name)
            if player.history[-1] > 0:
                player.wins -= 1
            elif player.history[-1] < 0:
                player.losses -= 1
            player.money -= player.history.pop()
        save_data()
        return self.play()

if __name__ == "__main__":
    MoneyMatch().run()