import random
import string
import tkinter as tk
from tkinter import messagebox

# Word bank to pull random words from for new games
WORD_BANK = [
    "PYTHON", "TKINTER", "CODING", "SEARCH", "PUZZLE",
    "ALGORITHM", "VARIABLE", "FUNCTION", "BOOLEAN", "COMPILER",
    "SOFTWARE", "DEVELOPER", "KEYBOARD", "COMPUTER", "PROGRAM",
    "DATABASE", "TERMINAL", "NETWORK", "HARDWARE", "SEQUENCE"
]

class WordSearchGUI:
    def __init__(self, root, grid_size=10, max_mistakes=10):
        self.root = root
        self.root.title("Python Tkinter Word Search")
        
        # Difficulty parameters
        self.grid_size = grid_size
        self.num_words_to_use = 5
        self.max_mistakes = max_mistakes
        
        self.start_new_game(increase_difficulty=False)

    def start_new_game(self, increase_difficulty=False):
        """Resets the board state and initializes layout."""
        if increase_difficulty:
            self.grid_size += 2  # Make grid bigger
            self.num_words_to_use = min(len(WORD_BANK), self.num_words_to_use + 2)  # Add more words
            
        # Select random words from bank
        self.words = [w.upper() for w in random.sample(WORD_BANK, self.num_words_to_use)]
        self.found_words = set()
        self.mistakes_left = self.max_mistakes
        self.selected_cells = []
        self.buttons = {}
        
        # Clear existing widgets from window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Build Game Data & UI
        self.grid = [['.' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generate_board()
        self.create_widgets()

    def generate_board(self):
        """Places words into the grid and fills remaining spots with letters."""
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Right, Down, Diagonals
        
        for word in self.words:
            placed = False
            attempts = 0
            while not placed and attempts < 200:
                d_row, d_col = random.choice(directions)
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                
                can_place = True
                for i in range(len(word)):
                    r, c = row + i * d_row, col + i * d_col
                    if not (0 <= r < self.grid_size and 0 <= c < self.grid_size):
                        can_place = False
                        break
                    if self.grid[r][c] != '.' and self.grid[r][c] != word[i]:
                        can_place = False
                        break
                        
                if can_place:
                    for i in range(len(word)):
                        r, c = row + i * d_row, col + i * d_col
                        self.grid[r][c] = word[i]
                    placed = True
                attempts += 1

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == '.':
                    self.grid[r][c] = random.choice(string.ascii_uppercase)

    def create_widgets(self):
        """Builds GUI components."""
        grid_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

        side_frame = tk.Frame(self.root, padx=10, pady=10)
        side_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Lives Counter
        self.mistakes_label = tk.Label(
            side_frame, 
            text=f"Mistakes Left: {self.mistakes_left}/{self.max_mistakes}", 
            font=("Helvetica", 12, "bold"), 
            fg="#c0392b"
        )
        self.mistakes_label.pack(anchor="w", pady=(0, 10))

        # Word List Header
        tk.Label(side_frame, text="FIND THESE WORDS:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        self.word_labels = {}
        for word in self.words:
            lbl = tk.Label(side_frame, text=f"• {word}", font=("Helvetica", 11), fg="black")
            lbl.pack(anchor="w", pady=2)
            self.word_labels[word] = lbl

        # Action Buttons
        check_btn = tk.Button(side_frame, text="Submit Word", font=("Helvetica", 10, "bold"), bg="#27ae60", fg="white", command=self.check_selected_word)
        check_btn.pack(pady=(15, 5), fill=tk.X)

        clear_btn = tk.Button(side_frame, text="Clear Selection", font=("Helvetica", 10), command=self.clear_selection)
        clear_btn.pack(pady=5, fill=tk.X)

        new_game_btn = tk.Button(side_frame, text="New Game (Harder)", font=("Helvetica", 10, "bold"), bg="#2980b9", fg="white", command=lambda: self.start_new_game(increase_difficulty=True))
        new_game_btn.pack(pady=(15, 0), fill=tk.X)

        # Board Grid Buttons
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                btn = tk.Button(
                    grid_frame,
                    text=self.grid[r][c],
                    font=("Helvetica", 11, "bold"),
                    width=3,
                    height=1,
                    bg="#ecf0f1",
                    command=lambda row=r, col=c: self.on_cell_click(row, col)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = btn

    def on_cell_click(self, row, col):
        """Selects individual letters."""
        cell = (row, col)
        
        if cell in self.selected_cells:
            return

        self.selected_cells.append(cell)
        self.buttons[cell].config(bg="#f1c40f")  # Highlight selection yellow

    def check_selected_word(self):
        """Validates the currently selected path when 'Submit Word' is clicked."""
        if not self.selected_cells:
            return

        selected_text = "".join(self.grid[r][c] for r, c in self.selected_cells)
        
        if selected_text in self.words and selected_text not in self.found_words:
            # CORRECT GUESS
            self.found_words.add(selected_text)
            
            # Color buttons green & disable them
            for r, c in self.selected_cells:
                self.buttons[(r, c)].config(bg="#2ecc71", fg="white", state="disabled")
                
            # Cross out the word in the list
            self.word_labels[selected_text].config(fg="gray", font=("Helvetica", 11, "overstrike"))
            self.selected_cells.clear()

            # Win check
            if len(self.found_words) == len(self.words):
                messagebox.showinfo("Victory!", "You found all the words!")
        else:
            # INCORRECT GUESS / MISTAKE
            self.mistakes_left -= 1
            self.mistakes_label.config(text=f"Mistakes Left: {self.mistakes_left}/{self.max_mistakes}")
            self.clear_selection()

            if self.mistakes_left <= 0:
                messagebox.showerror("Game Over", "You ran out of chances! Click 'New Game' to try again.")
                # Disable all remaining buttons
                for btn in self.buttons.values():
                    btn.config(state="disabled")

    def clear_selection(self):
        """Resets active highlighted cells."""
        for r, c in self.selected_cells:
            if self.buttons[(r, c)]["state"] != "disabled":
                self.buttons[(r, c)].config(bg="#ecf0f1")
        self.selected_cells.clear()

# --- RUN APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = WordSearchGUI(root)
    root.mainloop()
