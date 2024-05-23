import os

is_game_on = True
board_values = [' ', ' ',' ',' ',' ',' ',' ',' ',' ']
player_turn = 1
players_obj = {1: None, 2: None}
clear = lambda: os.system('cls')

def validation_input(message, possible_answers):
    answer =  input(message)
    while answer not in possible_answers:
        print("Incorrect value, try again :(")
        answer =  input(message)
    return answer

def define_players_letters () :
    player_one = validation_input('Player 1, select letter, please (x or o): ', ['x', 'o'])
    player_two = 'o' if player_one == 'x' else 'x'
    return {1: player_one, 2: player_two}

def display_board():
    clear()
    print(' {} | {} | {} '.format(board_values[0], board_values[1], board_values[2]))
    print('___________')
    print(' {} | {} | {} '.format(board_values[3], board_values[4], board_values[5]))
    print('___________')
    print(' {} | {} | {} '.format(board_values[6], board_values[7], board_values[8]))

def ask_for_action(player_number, board_values):
    question = f'Player {player_number}, select where to put {players_obj[player_number]}: (1-9) '
    possible_answers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    index_to_update = validation_input(question, possible_answers)
    while board_values[int(index_to_update)-1] != ' ':
        print('This spot is occupied already :)')
        index_to_update = validation_input(question, possible_answers)
    return update_board_values(index_to_update, board_values, player_number)

def update_board_values(index_to_update, current_board, player_number):
   current_board[int(index_to_update)-1] = players_obj[player_number]
   return current_board

def check_for_finish(mark):
    is_won =  ((board_values[0] == mark and board_values[1] == mark and board_values[2] == mark) or
    (board_values[3] == mark and board_values[4] == mark and board_values[5] == mark) or
    (board_values[6] == mark and board_values[7] == mark and board_values[8] == mark) or
    (board_values[0] == mark and board_values[3] == mark and board_values[6] == mark) or
    (board_values[1] == mark and board_values[4] == mark and board_values[7] == mark) or
    (board_values[2] == mark and board_values[5] == mark and board_values[8] == mark) or
    (board_values[0] == mark and board_values[4] == mark and board_values[8] == mark) or
    (board_values[2] == mark and board_values[4] == mark and board_values[6] == mark))

    is_tie = ' ' not in board_values
    if is_won:
        return 'player_won'
    elif is_tie:
        return 'tie'
    else:
        return False

def update_player_turn(current_player_number):
    if current_player_number == 1:
        return 2
    else:
        return 1
    
while is_game_on:
    if players_obj[1] == None:
        players_obj = define_players_letters()
    display_board()
    board_values = ask_for_action(player_turn, board_values)
    finish_result = check_for_finish(players_obj[player_turn])
    if (finish_result != False):
        finish_message = f'Player {player_turn} has won!! Congrats! Restart the game? (y / n): '
        if (finish_result == 'tie'):
             finish_message = f'Uff, its a tie! Restart the game? (y / n): '
        display_board()
        to_continue = validation_input(finish_message, ['y', 'n'])
        if to_continue == 'y':
            clear()
            board_values = [' ', ' ',' ',' ',' ',' ',' ',' ',' ']
            player_turn = 1
            players_obj = {1: None, 2: None}
        else:
            print('Thanks for playing! See you!')
            is_game_on = False
    else:
        player_turn = update_player_turn(player_turn)


