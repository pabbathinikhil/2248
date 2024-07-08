#!/usr/bin/env python
# coding: utf-8

# In[6]:


import tkinter as tk
import random
import math

class Game2248:
    def __init__(self, master):
        self.master = master
        self.master.title("2248 Game")
        
        # Game settings
        self.board_size = 4
        self.tile_size = 100
        self.target_value = 2048
        self.selected_tiles = []
        
        # Initialize the frames
        self.start_frame = tk.Frame(master)
        self.game_frame = tk.Frame(master)
        self.gameover_frame = tk.Frame(master)

        # Start screen widgets
        self.start_label = tk.Label(self.start_frame, text="Welcome to 2248 Game", font=("Arial", 24))
        self.start_label.pack(pady=20)
        self.start_button = tk.Button(self.start_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        # Game screen widgets
        self.win_label = tk.Label(self.game_frame, text=f"Target: {self.target_value}", font=("Arial", 16))
        self.win_label.pack()
        self.canvas = tk.Canvas(self.game_frame, width=self.board_size * self.tile_size, height=self.board_size * self.tile_size)
        self.canvas.pack()
        self.reset_button = tk.Button(self.game_frame, text="Restart", command=self.reset_game)
        self.reset_button.pack(pady=10)

        # Game over screen widgets
        self.gameover_label = tk.Label(self.gameover_frame, text="Game Over", font=("Arial", 24))
        self.gameover_label.pack(pady=20)
        self.retry_button = tk.Button(self.gameover_frame, text="Try Again", command=self.start_game)
        self.retry_button.pack(pady=10)

        # Bindings for game interactions
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Initial frame setup
        self.start_frame.pack(fill=tk.BOTH, expand=True)

    def start_game(self):
        self.reset_game()
        self.switch_frame(self.game_frame)

    def reset_game(self):
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.prefill_board()
        self.draw_board()
        self.check_win()

    def prefill_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = random.choice([2, 4, 8,16,32,64])

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.board_size):
            for j in range(self.board_size):
                value = self.board[i][j]
                color = self.get_tile_color(value)
                self.canvas.create_rectangle(j * self.tile_size, i * self.tile_size,
                                             (j + 1) * self.tile_size, (i + 1) * self.tile_size,
                                             fill=color, outline="black")
                if value != 0:
                    self.canvas.create_text(j * self.tile_size + self.tile_size / 2,
                                            i * self.tile_size + self.tile_size / 2,
                                            text=str(value), font=("Arial", 24, "bold"))

    def get_tile_color(self, value):
        colors = {
            0: "white", 2: "lightgray", 4: "lightblue", 8: "lightgreen",
            16: "yellow", 32: "orange", 64: "red", 128: "purple",
            256: "pink", 512: "brown", 1024: "cyan", 2048: "gold",
            4096: "lightcoral", 8192: "lightseagreen", 16384: "lightsteelblue"
        }
        return colors.get(value, "black")

    def on_click(self, event):
        self.selected_tiles = []
        self.select_tile(event)

    def on_drag(self, event):
        self.select_tile(event)

    def on_release(self, event):
        self.merge_selected_tiles()

    def select_tile(self, event):
        row = event.y // self.tile_size
        col = event.x // self.tile_size
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if not self.selected_tiles or (self.selected_tiles[-1] != (row, col) and self.board[row][col] != 0):
                if not self.selected_tiles or self.board[row][col] == self.board[self.selected_tiles[-1][0]][self.selected_tiles[-1][1]]:
                    self.selected_tiles.append((row, col))
                    self.highlight_selected_tiles()

    def highlight_selected_tiles(self):
        self.draw_board()
        for row, col in self.selected_tiles:
            self.canvas.create_rectangle(col * self.tile_size, row * self.tile_size,
                                         (col + 1) * self.tile_size, (row + 1) * self.tile_size,
                                         outline="blue", width=3)

    def merge_selected_tiles(self):
        if len(self.selected_tiles) < 2:
            return
        sum_value = sum(self.board[row][col] for row, col in self.selected_tiles)
        if sum_value == 0:
            return
        
        # Find the nearest power of 2 less than or equal to sum_value
        nearest_power = 2 ** math.floor(math.log2(sum_value))
        if nearest_power == sum_value:
            result_value = sum_value
        else:
            result_value = nearest_power
        
        for row, col in self.selected_tiles:
            self.board[row][col] = 0
        empty_tiles = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = result_value
        self.add_random_tiles(len(self.selected_tiles) - 1)  # Add (n-1) random tiles after merging
        self.draw_board()
        self.check_win()
        if self.check_game_over():
            self.switch_frame(self.gameover_frame)

    def add_random_tiles(self, count=1):
        empty_tiles = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == 0]
        for _ in range(count):
            if empty_tiles:
                i, j = random.choice(empty_tiles)
                self.board[i][j] = random.choice([2, 4])
                empty_tiles.remove((i, j))

    def check_win(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == self.target_value:
                    self.win_label.config(text=f"Target: {self.target_value} - You Win!")
                    return True
        self.win_label.config(text=f"Target: {self.target_value}")
        return False

    def check_game_over(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return False
                # Check right
                if j + 1 < self.board_size and self.board[i][j] == self.board[i][j + 1]:
                    return False
                # Check down
                if i + 1 < self.board_size and self.board[i][j] == self.board[i + 1][j]:
                    return False
                # Check left
                if j - 1 >= 0 and self.board[i][j] == self.board[i][j - 1]:
                    return False
                # Check up
                if i - 1 >= 0 and self.board[i][j] == self.board[i - 1][j]:
                    return False
                # Check top-left diagonal
                if i - 1 >= 0 and j - 1 >= 0 and self.board[i][j] == self.board[i - 1][j - 1]:
                    return False
                # Check top-right diagonal
                if i - 1 >= 0 and j + 1 < self.board_size and self.board[i][j] == self.board[i - 1][j + 1]:
                    return False
                # Check bottom-left diagonal
                if i + 1 < self.board_size and j - 1 >= 0 and self.board[i][j] == self.board[i + 1][j - 1]:
                    return False
                # Check bottom-right diagonal
                if i + 1 < self.board_size and j + 1 < self.board_size and self.board[i][j] == self.board[i + 1][j + 1]:
                    return False
        return True

    def switch_frame(self, frame):
        self.start_frame.pack_forget()
        self.game_frame.pack_forget()
        self.gameover_frame.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2248(root)
    root.mainloop()


# In[ ]:





# In[ ]:




