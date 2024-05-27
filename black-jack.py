from random import shuffle
import os

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
    
class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.balance = 0
        self.current_points = 0
        self.current_cards = []
    def __str__(self) -> str:
        return f'{self.name}, balance: {self.balance}, current hand: {self.current_cards}, points: {self.current_points}'
    
    def place_bet(self, amount):
        if self.balance < amount:
            print(f'Your balance is too low! Current balance - {self.balance}')
        else:     
            self.balance -= amount
            print(f'Your bet is placed!')

    def receive_money(self, amount):
        self.balance += amount

    def hit_another_card (self):
        new_player_card = deck.all_cards.pop(0)
        self.current_cards.append(new_player_card)
        self.count_player_points()
        self.display_player_cards()

    def count_player_points (self):
        self.current_points = 0
        for card in self.current_cards:
            self.current_points += card.value

    def display_player_cards (self):
        clear()
        print(f'Points: {self.current_points}')
        print('Your cards:')
        
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


player = Player(input('Welcome to the Black Jack! Enter your name: '))

while True: 
    try:
        player.receive_money(int(input("Enter your initial balance: ")))
    except:
        print('You must select number using 0-9')
    else:
        break

deck = Deck()
deck.shuffle()

while True: 
    try:
        player.place_bet(int(input(f"Please place your bet (from 1 to {player.balance}): ")))
    except:
        print('You must select number using 0-9')
    else:
        break
player.hit_another_card()

player_decision = input('Stand or hit? (s / h): ')
while player_decision == 'h':
    player.hit_another_card()
    player_decision = input('Stand or hit? (s / h): ')
if player_decision == 's':
    print(f'Got it. You decided to stay with {player.current_points} points')

# 1) welcome message + 
# 2) select name and initial balance + 
# 3) place bet + 
# 4) show current cards on hand and propose stand or hit
# 5) if hit show another card and ask again,
#     if stand - dealer starts to pick cards
#     if player 21 - win round
#     if player more than 21 - lose round
#     if dealer > player - lose round
#     if player > dealr - win round
# 6) start over again
