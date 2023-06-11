import tkinter as tk
from random import randint

# Constants
BOARD_SIZE = 10
SHIP_LENGTHS = [5, 4, 3, 2, 2]  # Different ship lengths
NUM_SHIPS = len(SHIP_LENGTHS)
NUM_SHOTS = 50

# Initialize game board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
ships = []
sunk_ships = 0
hits = 0
misses = 0

# Place ships randomly on the board
for length in SHIP_LENGTHS:
    ship = []
    while len(ship) < length:
        row = randint(0, BOARD_SIZE - 1)
        col = randint(0, BOARD_SIZE - 1)
        orientation = randint(0, 1)  # 0: horizontal, 1: vertical

        # Check if ship placement is valid
        valid = True
        for i in range(length):
            if (
                (orientation == 0 and col + i >= BOARD_SIZE) or
                (orientation == 1 and row + i >= BOARD_SIZE) or
                board[row][col + i] != ' ' or
                board[row + i][col] != ' '
            ):
                valid = False
                break

        if valid:
            for i in range(length):
                if orientation == 0:
                    ship.append((row, col + i))
                    board[row][col + i] = 'S'
                else:
                    ship.append((row + i, col))
                    board[row + i][col] = 'S'
            ships.append(ship)

# Create GUI
root = tk.Tk()
root.title("Battleship")
root.configure(bg='#303030')  # Darker background color

def click(row, col):
    global sunk_ships, hits, misses

    if board[row][col] == 'S':
        button = tk.Button(root, bg='green')
        button.grid(row=row, column=col, padx=2, pady=2)
        button.configure(state='disabled')
        board[row][col] = 'X'
        hits += 1

        # Check if ship is sunk
        for ship in ships:
            if (row, col) in ship:
                for tile in ship:
                    if board[tile[0]][tile[1]] != 'X':
                        break
                else:
                    sunk_ships += 1

        # Check if all ships are sunk
        if sunk_ships == NUM_SHIPS:
            end_label.config(text="You win!")

    elif board[row][col] == 'X':
        button = tk.Button(root, bg='green')
        button.grid(row=row, column=col, padx=2, pady=2)
        button.configure(state='disabled')
        hits += 1

    else:
        button = tk.Button(root, bg='red')
        button.grid(row=row, column=col, padx=2, pady=2)
        button.configure(state='disabled')
        board[row][col] = 'O'
        misses += 1

    # Update scoreboard
    hits_label.config(text=f"Hits: {hits}")
    misses_label.config(text=f"Misses: {misses}")

# Add scoreboard
score_frame = tk.Frame(root, bg='#303030')
score_frame.grid(row=BOARD_SIZE, columnspan=BOARD_SIZE, pady=10)

hits_label = tk.Label(score_frame, text=f"Hits: {hits}", font=("Arial", 12), fg='green', bg='#303030')
hits_label.pack(side=tk.LEFT, padx=10)

misses_label = tk.Label(score_frame, text=f"Misses: {misses}", font=("Arial", 12), fg='red', bg='#303030')
misses_label.pack(side=tk.LEFT, padx=10)

# Create game board
for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
        button = tk.Button(root, bg='#616161', relief=tk.RAISED, width=2, height=1)
        button.grid(row=row, column=col, padx=2, pady=2)
        button.configure(command=lambda row=row, col=col: click(row, col))

# Create end game label
end_label = tk.Label(root, text="", font=("Arial", 16), bg='#303030', fg='white')
end_label.grid(row=BOARD_SIZE+1, columnspan=BOARD_SIZE, pady=10)

root.mainloop()
