from random import shuffle
import os, time

suits = ["♦", "♣", "♠", "♥"]
nominals = {"    2": 2, "    3": 3, "    4": 4, "    5": 5, "    6": 6, "    7": 7, "    8": 8, "    9": 9, "   10": 10, " Jack": 10, "Queen": 10, "  King": 10, "  Ace": 11}
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
            print(f'Your balance is too low! Current balance - {self.balance}')
            raise Exception()
        else:     
            self.current_bet = amount
            self.balance -= amount
            print(f'Your bet is placed!')

    def update_money(self, amount):
        self.balance += amount

    def hit_another_card (self):
        new_player_card = deck.all_cards.pop(0)
        self.current_cards.append(new_player_card)
        self.count_player_points()

    def count_player_points (self):
        self.current_points = 0
        for card in self.current_cards:
            self.current_points += card.value
        self.display_player_cards()

    def display_player_cards (self):
        clear()
        print(f"{self.name}'s points: {self.current_points}")
        print(f"{self.name}'s cards:")
        
        rows_to_print = ['', '', '', '', '', '', '']
        for card in self.current_cards:
            rows_to_print[0] += '----------  '
            rows_to_print[1] += '|        |  '
            rows_to_print[2] += '|        |  '
            rows_to_print[3] += f' {card}    '
            rows_to_print[4] += '|        |  '
            rows_to_print[5] += '|        |  '
            rows_to_print[6] += '----------  '
        for row in rows_to_print:
            print(row)

    def reset_cards (self):
        self.current_cards = []
        self.current_points = 0

player = Player(input('Welcome to the Black Jack! Enter your name: '))

while True: 
    try:
        player.update_money(int(input("Enter your initial balance: ")))
    except:
        print('You must select number using 0-9')
    else:
        break


while game_on:
    if player.balance == 0:
        print('You do not have money :( Come back when you will have some more')
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
    
    player.hit_another_card()

    player_decision = input('Stand or hit? (s / h): ')

    while player_decision != 's':
        if player_decision == 'h':
            player.hit_another_card()
            if player.current_points == 21:
                print(f'Wow! You won {player.current_bet * 2}!')
                player.update_money(player.current_bet * 2)
                break
                
            if player.current_points > 21:
                for card in player.current_cards:
                    if card.value == 11:
                        card.change_ace_value()
                        player.count_player_points()
                if player.current_points > 21:
                    print(f'How sad :( You lost your bet of {player.current_bet}')
                    break
            player_decision = input('Stand or hit? (s / h): ')

        if player_decision not in ['s', 'h']:
            print('You must enter either "s" or "h"')
            player_decision = input('Stand or hit? (s / h): ')
    if player_decision == 's':
        print(f'Got it. You decided to stay with {player.current_points} points. Its dealers turn..')
        time.sleep(3)
        dealer = Player('Dealer')
        player_condition_to_win = player.current_points > dealer.current_points
        while player_condition_to_win: 
            dealer.hit_another_card()
            if dealer.current_points == 21:
                print(f'Dealer won.. You lost {player.current_bet}')
                break

            if dealer.current_points > 21:
                for card in dealer.current_cards:
                    if card.value == 11:
                        card.change_ace_value()
                        dealer.count_player_points()
                if dealer.current_points > 21:
                    print(f'Wow! {player.name} won {player.current_bet * 2}!')
                    player.update_money(player.current_bet * 2)
                    break
            elif dealer.current_points > player.current_points:
                print(f'Dealer has {dealer.current_points} points and {player.name} has {player.current_points} points.. Dealer won, you lost your bet')
                break
