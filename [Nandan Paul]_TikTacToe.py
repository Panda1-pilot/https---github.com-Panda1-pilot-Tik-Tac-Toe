import tkinter as tk
import random

player_score = 0
computer_score = 0
draw_score = 0
current_round = 1
board = [" " for _ in range(9)]


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return -10 + depth
    if winner == "O":
        return 10 - depth
    if " " not in board:
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def reset_board():
    """Reset the board for a new game."""
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", state="normal")
    status_label.config(text=f"Round {current_round}: Your turn (X)")

def check_winner(board):
    """Check for a winner or a draw."""
    for combo in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]
    if " " not in board:
        return "Tie"
    return None

def end_round(winner):
    """End the current round, update scores, and prepare for the next."""
    global player_score, computer_score, draw_score, current_round
    if winner == "X":
        player_score += 1
        status_label.config(text="You win this round!")
    elif winner == "O":
        computer_score += 1
        status_label.config(text="Computer wins this round!")
    else:
        draw_score += 1
        status_label.config(text="This round is a draw!")

    for btn in buttons:
        btn.config(state="disabled")

    current_round += 1
    root.after(2000, reset_board)

def make_move(pos, button):
    """Handle the player's move."""
    if board[pos] == " ":
        board[pos] = "X"
        button.config(text="X")
        winner = check_winner(board)
        if winner:
            end_round(winner)
            return
        computer_move()

def computer_move():
    """Handle the computer's move."""
    pos = best_move(board)
    board[pos] = "O"
    buttons[pos].config(text="O")
    winner = check_winner(board)
    if winner:
        end_round(winner)

def quit_game():
    """Display results and quit the game."""
    result_text = (f"Final Results:\n"
                   f"Rounds Played: {current_round - 1}\n"
                   f"Player Wins: {player_score}\n"
                   f"Computer Wins: {computer_score}\n"
                   f"Draws: {draw_score}")
    status_label.config(text=result_text)
    for btn in buttons:
        btn.config(state="disabled")

root = tk.Tk()
root.title("Tic-Tac-Toe")

status_label = tk.Label(root, text="Round 1: Your turn (X)", font=("Arial", 14))
status_label.pack()

frame = tk.Frame(root)
frame.pack()
buttons = []


for i in range(3):
    for j in range(3):
        btn = tk.Button(frame, text=" ", font=("Arial", 20), width=5, height=2)
        btn.grid(row=i, column=j)
        buttons.append(btn)

for i, btn in enumerate(buttons):
    btn.config(command=lambda i=i, btn=btn: make_move(i, btn))

quit_button = tk.Button(root, text="Quit", font=("Arial", 14), command=quit_game)
quit_button.pack()


root.mainloop()
