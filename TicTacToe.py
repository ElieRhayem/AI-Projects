# Rodolph Khoury - 222199
# Elie Rhayem - 222555

import tkinter as tk
from tkinter import ttk
import time
from typing import List, Tuple, Optional

class TicTacToe4x4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe 4x4")
        
        self.board = [['' for _ in range(4)] for _ in range(4)]
        self.current_player = 'O'
        self.game_over = False
        
        self.difficulty_depths = {
            'Easy': 1,
            'Medium': 3,
            'Hard': 5
        }
        self.current_depth = self.difficulty_depths['Medium']
        
        self.create_gui()
        
    def create_gui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Difficulty:").grid(row=0, column=0, padx=5, pady=5)
        self.difficulty_var = tk.StringVar(value='Medium')
        difficulty_menu = ttk.OptionMenu(
            main_frame,
            self.difficulty_var,
            'Medium',
            *self.difficulty_depths.keys(),
            command=self.change_difficulty
        )
        difficulty_menu.grid(row=0, column=1, padx=5, pady=5)
        
        board_frame = ttk.Frame(main_frame)
        board_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.buttons = []
        for i in range(4):
            row_buttons = []
            for j in range(4):
                button = ttk.Button(
                    board_frame,
                    text='',
                    width=5,
                    command=lambda r=i, c=j: self.make_move(r, c)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        self.status_label = ttk.Label(main_frame, text="Human turn (O)")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            main_frame,
            text="Reset Game",
            command=self.reset_game
        ).grid(row=3, column=0, columnspan=2, pady=5)

    def change_difficulty(self, difficulty):
        self.current_depth = self.difficulty_depths[difficulty]
        self.reset_game()
        
    def reset_game(self):
        self.board = [['' for _ in range(4)] for _ in range(4)]
        self.current_player = 'O'
        self.game_over = False
        for row in self.buttons:
            for button in row:
                button['text'] = ''
        self.status_label['text'] = "Human turn (O)"
        
    def make_move(self, row: int, col: int):
        if self.game_over or self.board[row][col] != '':
            return
            
        self.board[row][col] = 'O'
        self.buttons[row][col]['text'] = 'O'
        
        if self.check_winner('O'):
            self.game_over = True
            self.status_label['text'] = "You win!"
            return
            
        if self.is_board_full():
            self.game_over = True
            self.status_label['text'] = "It's a draw!"
            return
            
        self.status_label['text'] = "AI is thinking..."
        self.window.update()
        
        start_time = time.time()
        ai_move = self.get_best_move()
        if ai_move:
            ai_row, ai_col = ai_move
            self.board[ai_row][ai_col] = 'X'
            self.buttons[ai_row][ai_col]['text'] = 'X'
            
        if self.check_winner('X'):
            self.game_over = True
            self.status_label['text'] = "AI wins!"
            return
            
        if self.is_board_full():
            self.game_over = True
            self.status_label['text'] = "It's a draw!"
            return
            
        elapsed_time = time.time() - start_time
        self.status_label['text'] = f"Human turn (O) - AI took {elapsed_time:.2f}s"
        
    def get_best_move(self) -> Optional[Tuple[int, int]]:
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == '':
                    self.board[i][j] = 'X'
                    score = self.minimax(self.current_depth - 1, False, alpha, beta, True)
                    self.board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                        
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
                        
        return best_move
        
    def minimax(self, depth: int, is_maximizing: bool, alpha: float, beta: float, use_prunning: bool) -> float:
        if self.check_winner('X'):
            return 100 + depth
        if self.check_winner('O'):
            return -100 - depth
        if self.is_board_full() or depth == 0:
            return self.evaluate_board()
            
        if is_maximizing:
            max_eval = float('-inf')
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        eval = self.minimax(depth - 1, False, alpha, beta, use_prunning)
                        self.board[i][j] = ''
                        max_eval = max(max_eval, eval)
                        if use_prunning:
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break 
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        eval = self.minimax(depth - 1, True, alpha, beta, use_prunning)
                        self.board[i][j] = ''
                        min_eval = min(min_eval, eval)
                        if use_prunning:
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return min_eval
            
    def evaluate_board(self) -> float:
        score = 0
        
        for row in self.board:
            score += self.evaluate_line(row)
            
        for col in range(4):
            column = [self.board[row][col] for row in range(4)]
            score += self.evaluate_line(column)
            
        diagonal1 = [self.board[i][i] for i in range(4)]
        diagonal2 = [self.board[i][3-i] for i in range(4)]
        score += self.evaluate_line(diagonal1)
        score += self.evaluate_line(diagonal2)
        
        return score
        
    def evaluate_line(self, line: List[str]) -> float:
        score = 0
        
        x_count = line.count('X')
        o_count = line.count('O')
        
        if o_count == 0 and x_count > 0:
            score += pow(10, x_count)
        elif x_count == 0 and o_count > 0:
            score -= pow(10, o_count)
            
        return score
        
    def check_winner(self, player: str) -> bool:
        for row in self.board:
            if all(cell == player for cell in row):
                return True
                
        for col in range(4):
            if all(self.board[row][col] == player for row in range(4)):
                return True
                
        if all(self.board[i][i] == player for i in range(4)):
            return True
        if all(self.board[i][3-i] == player for i in range(4)):
            return True
            
        return False
        
    def is_board_full(self) -> bool:
        return all(all(cell != '' for cell in row) for row in self.board)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe4x4()
    game.run()
 