from random import shuffle
import os, time

suits = ["♦", "♣", "♠", "♥"]
nominals = {"    2": 2, "    3": 3, "    4": 4, "    5": 5, "    6": 6, "    7": 7, "    8": 8, "    9": 9, "   10": 10, " Jack": 10, "Queen": 10,"  King": 10, "  Ace": 11}
game_on = True
clear = lambda: os.system('cls')

class Deck:
    all_cards = []
    def __init__ (self):
        for suit in suits:
            for nominal in nominals.keys():
                self.all_cards.append(Card(suit, nominal, nominals[nominal]))
    def shuffle (self):
        shuffle(self.all_cards)

class Card:
    def __init__(self, suit, nominal, value):
        self.suit = suit
        self.nominal = nominal 
        self.value = value
    def __str__(self) -> str:
        return f'{self.nominal} {self.suit}'
    def change_ace_value (self):
        self.value = 1
    
class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.balance = 0
        self.current_points = 0
        self.current_cards = []
        self.current_bet = 0
    def __str__(self) -> str:
        return f'{self.name}, balance: {self.balance}, current hand: {self.current_cards}, points: {self.current_points}'
    
    def place_bet(self, amount):
        if self.balance < amount:
            print(f'Your balance is too low to place such bet! Current balance - {self.balance}')
            raise Exception()
        else:     
            self.current_bet = amount
            self.balance -= amount
            print('Bets placed, dealing cards..')

    def update_money(self, amount, wait_time = 3):
        self.balance += amount
        time.sleep(wait_time)

    def hit_another_card (self):
        new_player_card = deck.all_cards.pop(0)
        self.current_cards.append(new_player_card)
        self.count_player_points()

    def count_player_points (self):
        self.current_points = 0
        for card in self.current_cards:
            self.current_points += card.value

    def display_player_cards (self, is_last_card_hidden = False):
        print(f"{self.name}'s points: {self.current_points}")
        print(f"{self.name}'s cards:")
        
        rows_to_print = ['', '', '', '', '', '', '']
        for card in self.current_cards:
            rows_to_print[0] += ' --------   '
            rows_to_print[1] += '|        |  '
            rows_to_print[2] += '|        |  '
            rows_to_print[3] += f' {card}    '
            rows_to_print[4] += '|        |  '
            rows_to_print[5] += '|        |  '
            rows_to_print[6] += ' --------   '
        if is_last_card_hidden:
            rows_to_print[0] += ' --------   '
            rows_to_print[1] += '|--------|  '
            rows_to_print[2] += '|--------|  '
            rows_to_print[3] += '|-HIDDEN-|  '
            rows_to_print[4] += '|--------|  '
            rows_to_print[5] += '|--------|  '
            rows_to_print[6] += ' --------   '
        for row in rows_to_print:
            print(row)

    def reset_cards (self):
        self.current_cards = []
        self.current_points = 0
def display_game_table (hide_last_dealer_card = False):
    clear()
    dealer.display_player_cards(hide_last_dealer_card)
    print('                        ')
    print('                        ')
    print('                        ')
    player.display_player_cards()
player = Player(input('Welcome to the Black Jack! Enter your name: '))

while True: 
    try:
        player.update_money(int(input("Enter your initial balance: ")), 0)
    except:
        print('You must select number using 0-9')
    else:
        break


while game_on:
    if player.balance == 0:
        print('You do not have money :( Come back when you will have some more..')
        time.sleep(5)
        game_on = False
        break
    deck = Deck()
    deck.shuffle()
    player.reset_cards()
    print(f'{player.name}, your current balance is {player.balance}')
    while True: 
        try:
            player.place_bet(int(input(f"Please place your bet (from 1 to {player.balance}): ")))
        except:
            print('You must select number using 0-9')
        else:
            break
    time.sleep(3)
    dealer = Player('Dealer')
    dealer.hit_another_card()
    player.hit_another_card()
    player.hit_another_card()
    display_game_table(True)
    if player.current_points == 21:
        print(f'BLACK JACK! You won {player.current_bet * 2}!')
        player.update_money(player.current_bet * 2)
        break
    elif player.current_points > 21:
        for card in player.current_cards:
            if card.value == 11:
                card.change_ace_value()
                player.count_player_points()
                display_game_table(True)
        if player.current_points > 21:
            print(f'How sad, you Busted :( You lost your bet of {player.current_bet}..')
            time.sleep(3)
            break
    player_decision = input('Stand or hit? (s / h): ')

    while player_decision != 's':
        if player_decision == 'h':
            player.hit_another_card()
            display_game_table(True)
            if player.current_points == 21:
                print(f'Wow! You won {player.current_bet * 2}!')
                player.update_money(player.current_bet * 2)
                break
                
            if player.current_points > 21:
                for card in player.current_cards:
                    if card.value == 11:
                        card.change_ace_value()
                        player.count_player_points()
                        display_game_table(True)
                if player.current_points > 21:
                    print(f'How sad, you Busted :( You lost your bet of {player.current_bet}..')
                    time.sleep(3)
                    break
            player_decision = input('Stand or hit? (s / h): ')

        if player_decision not in ['s', 'h']:
            print('You must enter either "s" or "h"')
            player_decision = input('Stand or hit? (s / h): ')
    if player_decision == 's':
        print(f'Got it. You decided to stay with {player.current_points} points. Its dealers turn..')
        time.sleep(3)
        print('Dealer deals next card..')
        time.sleep(2)
        dealer.hit_another_card()
        display_game_table()
        time.sleep(3)
        while True: 
            if dealer.current_points >= 17:
                break
            dealer.hit_another_card()
            display_game_table()
            time.sleep(3)
           
        if dealer.current_points == 21:
                print(f'Dealer won.. You lost {player.current_bet}')
                time.sleep(3)
        elif dealer.current_points > 21:
            for card in dealer.current_cards:
                if card.value == 11:
                    card.change_ace_value()
                    dealer.count_player_points()
            if dealer.current_points > 21:
                print(f'Wow! Dealer is Busted! {player.name} won {player.current_bet * 2}!')
                player.update_money(player.current_bet * 2)
        elif dealer.current_points > player.current_points:
            print(f'Dealer has {dealer.current_points} points and {player.name} has {player.current_points} points.. Dealer won, you lost {player.current_bet}.')
            time.sleep(3)
        elif dealer.current_points < player.current_points:
            print(f'Dealer has {dealer.current_points} points and {player.name} has {player.current_points} points.. {player.name} won {player.current_bet * 2}, congrats!')
            player.update_money(player.current_bet * 2)
        elif dealer.current_points == player.current_points:
            print(f'It is a draw! Your bet is returning to you..')
            player.update_money(player.current_bet)