import math

# Initialize the board as a list of 9 empty spaces
board = [' ' for _ in range(9)]

def print_board():
    #Print the current state of the board
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def is_winner(board, player):
    #Check if the given player has won
    win_conditions = [
        [board[0], board[1], board[2]],  # Top row
        [board[3], board[4], board[5]],  # Middle row
        [board[6], board[7], board[8]],  # Bottom row
        [board[0], board[3], board[6]],  # Left column
        [board[1], board[4], board[7]],  # Middle column
        [board[2], board[5], board[8]],  # Right column
        [board[0], board[4], board[8]],  # Diagonal from top-left to bottom-right
        [board[2], board[4], board[6]],  # Diagonal from top-right to bottom-left
    ]
    return [player, player, player] in win_conditions

def is_board_full(board):
    #Check if the board is completely filled
    return ' ' not in board

def minimax(board, depth, alpha, beta, is_maximizing):

   # Implement the minimax algorithm with alpha-beta pruning
   # to determine the best move for the AI
    if is_winner(board, 'O'):
        return 1
    elif is_winner(board, 'X'):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move():
    #Determine the best move for the AI using the minimax algorithm
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

def play_game():
    #Main game loop
    print_board()
    while True:
        # Human move
        move = int(input("Enter your move (1-9): ")) - 1
        if board[move] != ' ':
            print("Invalid move! Try again.")
            continue
        board[move] = 'X'
        print_board()
        if is_winner(board, 'X'):
            print("You win!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

        # AI move
        move = best_move()
        board[move] = 'O'
        print("AI move:")
        print_board()
        if is_winner(board, 'O'):
            print("AI wins!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()
