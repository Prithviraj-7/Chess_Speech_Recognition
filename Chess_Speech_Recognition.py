import tkinter as tk
from tkinter import messagebox, simpledialog
import chess

# Unicode chess pieces
UNICODE_PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
}

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Game")
        self.geometry("720x930")
        self.board = chess.Board()
        self.selected_square = None
        self.buttons = {}

        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.board_frame = tk.Frame(self)
        self.board_frame.grid(row=0, column=0)

        for row in range(8):
            for col in range(8):
                btn = tk.Button(
                    self.board_frame, font=("Arial", 36), width=2, height=1,
                    command=lambda r=row, c=col: self.on_click(r, c),
                    relief="flat", bd=0
                )
                btn.grid(row=row, column=col)
                self.buttons[(row, col)] = btn

        self.log_box = tk.Text(self, width=25, height=20, font=("Arial", 12))
        self.log_box.grid(row=0, column=1, padx=10, pady=5)
        self.log_box.configure(state='disabled')

    def on_click(self, row, col):
        square = chess.square(col, 7 - row)
        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece and piece.color == self.board.turn:
                self.selected_square = square
        else:
            from_sq = self.selected_square
            to_sq = square
            move_made = False

            for move in self.board.legal_moves:
                if move.from_square == from_sq and move.to_square == to_sq:
                    if self.board.piece_at(from_sq).piece_type == chess.PAWN and move.promotion:
                        promo_piece = self.ask_promotion()
                        move = chess.Move(from_sq, to_sq, promotion=promo_piece)

                    self.log_move(move)  # Log before making move!
                    self.board.push(move)
                    self.check_game_status()
                    self.update_board()
                    move_made = True
                    break

            self.selected_square = None

    def ask_promotion(self):
        piece_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'n': chess.KNIGHT, 'b': chess.BISHOP}
        choice = simpledialog.askstring("Pawn Promotion", "Choose promotion (q, r, b, n):").lower()
        return piece_map.get(choice, chess.QUEEN)

    def update_board(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                symbol = UNICODE_PIECES.get(piece.symbol(), "") if piece else ""
                bg = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.buttons[(row, col)].config(text=symbol, bg=bg)

    def log_move(self, move):
        san = self.board.san(move)
        turn = (self.board.fullmove_number if self.board.turn == chess.BLACK else self.board.fullmove_number - 1)
        self.log_box.configure(state='normal')
        if self.board.turn == chess.BLACK:
            self.log_box.insert(tk.END, f"{turn}. {san} ")
        else:
            self.log_box.insert(tk.END, f"{san}\n")
        self.log_box.configure(state='disabled')
        self.log_box.yview(tk.END)

    def check_game_status(self):
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            messagebox.showinfo("Checkmate", f"{winner} wins by checkmate!")
            self.board.reset()
            self.log_box.configure(state='normal')
            self.log_box.insert(tk.END, "\n--- New Game ---\n")
            self.log_box.configure(state='disabled')
        elif self.board.is_stalemate():
            messagebox.showinfo("Stalemate", "It's a draw!")
            self.board.reset()
        elif self.board.is_check():
            print("Check!")

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()
