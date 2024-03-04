from tkinter import *
from tkinter.messagebox import *
import random

# Dictionary representing the Tic Tac Toe board with positions as keys and empty strings as initial values
board = {
    'UL': '', 'UM': '', 'UR': '',
    'ML': '', 'MM': '', 'MR': '',
    'LL': '', 'LM': '', 'LR': '',
}

# Dictionary mapping grid positions to board positions
positions = {
    (0, 0): 'UL', (0, 1): 'UM', (0, 2): 'UR',
    (1, 0): 'ML', (1, 1): 'MM', (1, 2): 'MR',
    (2, 0): 'LL', (2, 1): 'LM', (2, 2): 'LR',
}

# Variable to keep track of the current player ('X' or 'O')
current_player = 'X'


# Function to check if the board is full
def is_full():
    return '' not in board.values()


# Function to check if a player has won
def is_winner(user_symbol, board):
    # List of winning combinations
    winning_combinations = [
        ['UL', 'UM', 'UR'], ['ML', 'MM', 'MR'], ['LL', 'LM', 'LR'],  # Rows
        ['UL', 'ML', 'LL'], ['UM', 'MM', 'LM'], ['UR', 'MR', 'LR'],  # Columns
        ['UL', 'MM', 'LR'], ['UR', 'MM', 'LL']  # Diagonals
    ]
    # Check each winning combination
    for combo in winning_combinations:
        if all(board[i] == user_symbol for i in combo):
            return True

    return False


# Function to clear the board
def clear_board():
    for pos in board:
        board[pos] = ''


# Function to handle the 'play again' option
def play_again():
    global current_player
    answer = askyesno('play again', 'want to play again?')
    if not answer:
        exit()
    else:
        board_window.destroy()
        root.destroy()
        clear_board()
        current_player = 'X'
        start()


# Function for AI to make a move
def ai_play():
    global current_player
    move = ai_move()
    board[move] = current_player
    if is_full():
        showinfo('Draw', 'Draw!')
        play_again()
    if is_winner(current_player, board):
        showinfo('Winner', f'player {current_player} win!')
        play_again()
    buttons[move].config(text=current_player)
    buttons[move].config(state='disabled')
    current_player = 'X'
    turn_label.config(text=f"Player {current_player} Turn")


# Function to determine AI's move
def ai_move():
    possiblemoves = []
    # Find empty positions on the board
    for position in board:
        if board[position] == '':
            possiblemoves.append(position)
    if not possiblemoves:
        return
    else:
        # Check for winning moves
        for player in ['O', 'X']:
            for move in possiblemoves:
                boardcopy = board.copy()
                boardcopy[move] = player
                if is_winner(player, boardcopy):
                    return move
        # Prioritize corners, then edges
        corner = []
        for move in possiblemoves:
            if move in ['UL', 'UR', 'LL', 'LR']:
                corner.append(move)
        if len(corner) > 0:
            i = random.choice(corner)
            return i
        edge = []
        for move in possiblemoves:
            if move in ['ML', 'UM', 'MR', 'LM']:
                edge.append(move)
        if len(edge) > 0:
            i = random.choice(edge)
            return i


# Function to set window dimensions and position
def set_window(window):
    window_width = 400
    window_height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Function to handle button clicks
def button_clicked(pos, cp):
    global buttons, current_player
    if cp == 'Player':
        # Handle player's move
        board[pos] = current_player
        if is_full():
            showinfo('Draw', 'Draw!')
            play_again()
        if is_winner(current_player, board):
            showinfo('Winner', f'player {current_player} win!')
            play_again()
        buttons[pos].config(text=current_player)
        buttons[pos].config(state='disabled')
        current_player = 'O' if current_player == 'X' else 'X'
        turn_label.config(text=f"Player {current_player} Turn")
    elif cp == 'Computer':
        # Handle AI's move
        board[pos] = current_player
        if is_full():
            showinfo('Draw', 'Draw!')
            play_again()
        if is_winner(current_player, board):
            showinfo('Winner', f'player {current_player} win!')
            play_again()
        buttons[pos].config(text=current_player)
        buttons[pos].config(state='disabled')
        current_player = 'O'
        turn_label.config(text=f"Player {current_player} Turn")
        ai_play()


# Function to create the game window
def play_window(cp):
    global board, buttons, turn_label, board_window
    board_window = Tk()
    board_window.title('Tic Tac Toe')
    set_window(board_window)
    turn_label = Label(board_window, text=f"Player {current_player} Turn", font=("Arial", 16))
    turn_label.grid(row=0, column=1, pady=10)

    # Frame to contain the buttons
    button_container = Frame(board_window)
    button_container.grid(row=1, column=0, columnspan=3)
    buttons = {}
    for i in range(3):
        button_container.grid_rowconfigure(i, weight=1)
        button_container.grid_columnconfigure(i, weight=1)
    for i in range(3):
        for j in range(3):
            position = positions[(i, j)]
            buttons[position] = Button(button_container, text='', height=3, width=12,
                                       command=lambda pos=position: button_clicked(pos, cp))
            buttons[position].grid(row=i, column=j, padx=10, pady=10, sticky='nsew')

    # Update the layout and position the buttons in the center
    board_window.update_idletasks()
    x = (board_window.winfo_width() - button_container.winfo_width()) // 2
    y = (board_window.winfo_height() - button_container.winfo_height()) // 2
    button_container.grid_propagate(False)  # Disable frame resizing
    button_container.grid(padx=x, pady=y)

    board_window.mainloop()


# Function to start the game
def start():
    global root
    root = Tk()
    root.title('Tic Tac Toe')
    set_window(root)
    welcomeLabel = Label(root, text="Welcome to Tic Tac Toe game", font=24)
    welcomeLabel.pack()

    askLabel = Label(root, text="Choose your opponent", font=24)
    askLabel.pack()

    computerButton = Button(root, text="Computer", font=24, command=lambda: play_window('Computer'))

    playerButton = Button(root, text="Second player", font=24, command=lambda: play_window('Player'))

    # Place computerButton and playerButton at the bottom
    # Slightly above the end with space between them
    computerButton.place(relx=0.5, rely=0.6, anchor=CENTER)
    playerButton.place(relx=0.5, rely=0.8, anchor=CENTER)

    root.mainloop()


start()
