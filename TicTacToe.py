import math
import tkinter as tk
from tkinter import messagebox

HUMAN = "X"
AI = "O"
EMPTY = " "

WINDOW_TITLE = "CodSoft Task 2 - Tic-Tac-Toe AI"

BG = "#0f172a"
PANEL = "#111827"
CARD = "#1f2937"
TEXT = "#f8fafc"
MUTED = "#cbd5e1"
ACCENT = "#22c55e"
ACCENT2 = "#3b82f6"
DANGER = "#ef4444"
GOLD = "#f59e0b"
EMPTY_BTN = "#e5e7eb"
EMPTY_BTN_ACTIVE = "#d1d5db"
HUMAN_BG = "#bfdbfe"
HUMAN_FG = "#1d4ed8"
AI_BG = "#bbf7d0"
AI_FG = "#166534"
WIN_BG = "#f59e0b"
WIN_FG = "#111827"


def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)

    if EMPTY not in board:
        return "Draw", None

    return None, None


def minimax(board, depth, is_maximizing, alpha, beta):
    result, _ = check_winner(board)

    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = EMPTY
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = EMPTY
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score


def best_move(board):
    preferred_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    best_score = -math.inf
    move = None

    for i in preferred_order:
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i

    return move


class TicTacToeAI:
    def __init__(self, root):
        self.root = root

        # Responsive scaling based on screen size
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.scale = min(sw / 1366, sh / 768, 1.0)

        self.w = int(520 * self.scale)
        self.h = int(640 * self.scale)
        self.title_font = max(16, int(20 * self.scale))
        self.subtitle_font = max(8, int(9 * self.scale))
        self.status_font = max(11, int(13 * self.scale))
        self.button_font = max(18, int(22 * self.scale))
        self.control_font = max(9, int(10 * self.scale))
        self.card_score_font = max(13, int(16 * self.scale))
        self.card_label_font = max(8, int(9 * self.scale))

        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.minsize(self.w, self.h)
        self.root.maxsize(self.w, self.h)
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board = [EMPTY] * 9
        self.buttons = []
        self.game_over = False
        self.winning_combo = None

        self.human_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self._build_ui()
        self.new_round()

    def _build_ui(self):
        pad_x = max(12, int(16 * self.scale))
        pad_y_top = max(10, int(14 * self.scale))
        pad_y = max(4, int(6 * self.scale))
        board_pad = max(10, int(14 * self.scale))
        btn_pad_x = max(4, int(5 * self.scale))
        btn_pad_y = max(4, int(5 * self.scale))

        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=pad_x, pady=(pad_y_top, pad_y))

        title = tk.Label(
            header,
            text="Tic-Tac-Toe AI",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", self.title_font, "bold")
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Unbeatable Minimax AI",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", self.subtitle_font)
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Score cards
        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.pack(fill="x", padx=pad_x, pady=(4, 4))

        self.human_score_card = self._score_card(
            score_frame, "You", str(self.human_score), HUMAN_BG, HUMAN_FG
        )
        self.ai_score_card = self._score_card(
            score_frame, "AI", str(self.ai_score), AI_BG, AI_FG
        )
        self.draw_score_card = self._score_card(
            score_frame, "Draws", str(self.draw_score), "#e9d5ff", "#6b21a8"
        )

        self.human_score_card.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.ai_score_card.grid(row=0, column=1, sticky="ew", padx=6)
        self.draw_score_card.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        score_frame.columnconfigure((0, 1, 2), weight=1)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Your turn: X",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", self.status_font, "bold")
        )
        self.status_label.pack(pady=(4, 6))

        # Board area
        board_outer = tk.Frame(
            self.root,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground="#243041"
        )
        board_outer.pack(padx=pad_x, pady=(4, 8), fill="both", expand=False)

        board_title = tk.Label(
            board_outer,
            text="Tap a square to play",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", self.subtitle_font)
        )
        board_title.pack(pady=(10, 6))

        board_frame = tk.Frame(board_outer, bg=PANEL)
        board_frame.pack(padx=board_pad, pady=(0, board_pad))

        btn_size = max(3, int(4 * self.scale))
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                width=btn_size,
                height=max(2, int(2 * self.scale)),
                font=("Segoe UI", self.button_font, "bold"),
                bg=EMPTY_BTN,
                fg="#111827",
                activebackground=EMPTY_BTN_ACTIVE,
                activeforeground="#111827",
                relief="flat",
                bd=0,
                command=lambda idx=i: self.handle_move(idx),
                cursor="hand2"
            )
            btn.grid(row=i // 3, column=i % 3, padx=btn_pad_x, pady=btn_pad_y, ipadx=2, ipady=2)
            self.buttons.append(btn)

        # Controls
        control_frame = tk.Frame(self.root, bg=BG)
        control_frame.pack(fill="x", padx=pad_x, pady=(4, 6))

        control_pad_x = max(8, int(10 * self.scale))
        control_pad_y = max(6, int(8 * self.scale))

        self.play_again_btn = tk.Button(
            control_frame,
            text="Play Again",
            font=("Segoe UI", self.control_font, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=control_pad_x,
            pady=control_pad_y,
            cursor="hand2",
            command=self.play_again
        )
        self.play_again_btn.pack(side="left", padx=(0, 6))

        reset_btn = tk.Button(
            control_frame,
            text="Reset Scores",
            font=("Segoe UI", self.control_font, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=control_pad_x,
            pady=control_pad_y,
            cursor="hand2",
            command=self.reset_scores
        )
        reset_btn.pack(side="left", padx=(0, 6))

        help_btn = tk.Button(
            control_frame,
            text="How AI Works",
            font=("Segoe UI", self.control_font, "bold"),
            bg=CARD,
            fg="white",
            activebackground="#374151",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=control_pad_x,
            pady=control_pad_y,
            cursor="hand2",
            command=self.show_help
        )
        help_btn.pack(side="left")

        exit_btn = tk.Button(
            control_frame,
            text="Exit",
            font=("Segoe UI", self.control_font, "bold"),
            bg=DANGER,
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=control_pad_x,
            pady=control_pad_y,
            cursor="hand2",
            command=self.root.destroy
        )
        exit_btn.pack(side="right")

        footer = tk.Label(
            self.root,
            text="Human = X   |   AI = O   |   Minimax makes the AI unbeatable",
            bg=BG,
            fg="#94a3b8",
            font=("Segoe UI", max(7, int(8 * self.scale)))
        )
        footer.pack(side="bottom", pady=(0, 8))

    def _score_card(self, parent, label_text, value_text, bg_color, fg_color):
        card = tk.Frame(parent, bg=bg_color, padx=max(8, int(8 * self.scale)), pady=max(8, int(8 * self.scale)))
        tk.Label(
            card,
            text=label_text,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", self.card_label_font, "bold")
        ).pack()
        score_label = tk.Label(
            card,
            text=value_text,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", self.card_score_font, "bold")
        )
        score_label.pack()
        card.score_label = score_label
        return card

    def update_scores(self):
        self.human_score_card.score_label.config(text=str(self.human_score))
        self.ai_score_card.score_label.config(text=str(self.ai_score))
        self.draw_score_card.score_label.config(text=str(self.draw_score))

    def show_help(self):
        messagebox.showinfo(
            "How the AI Works",
            "This game uses the Minimax algorithm with Alpha-Beta pruning.\n\n"
            "The AI explores possible outcomes and picks the best move.\n"
            "That makes it unbeatable in Tic-Tac-Toe."
        )

    def new_round(self):
        self.board = [EMPTY] * 9
        self.game_over = False
        self.winning_combo = None
        self.status_label.config(text="Your turn: X", fg=ACCENT)

        for btn in self.buttons:
            btn.config(
                text="",
                state="normal",
                bg=EMPTY_BTN,
                fg="#111827",
                activebackground=EMPTY_BTN_ACTIVE
            )

    def play_again(self):
        self.new_round()

    def reset_scores(self):
        self.human_score = 0
        self.ai_score = 0
        self.draw_score = 0
        self.update_scores()
        self.new_round()

    def handle_move(self, index):
        if self.game_over or self.board[index] != EMPTY:
            return

        self.make_move(index, HUMAN)

        result, combo = check_winner(self.board)
        if self.finish_game_if_needed(result, combo):
            return

        self.status_label.config(text="AI is thinking...", fg=GOLD)
        self.disable_board()
        self.root.after(250, self.ai_turn)

    def make_move(self, index, player):
        self.board[index] = player
        if player == HUMAN:
            self.buttons[index].config(text=HUMAN, bg=HUMAN_BG, fg=HUMAN_FG)
        else:
            self.buttons[index].config(text=AI, bg=AI_BG, fg=AI_FG)

    def ai_turn(self):
        if self.game_over:
            return

        move = best_move(self.board)
        if move is not None:
            self.make_move(move, AI)

        result, combo = check_winner(self.board)
        if self.finish_game_if_needed(result, combo):
            return

        self.enable_board()
        self.status_label.config(text="Your turn: X", fg=ACCENT)

    def finish_game_if_needed(self, result, combo):
        if result is None:
            return False

        self.game_over = True
        self.winning_combo = combo
        self.disable_board()

        if combo:
            self.highlight_winning_combo(combo)

        if result == HUMAN:
            self.human_score += 1
            self.status_label.config(text="You win! 🎉", fg=ACCENT2)
            self.update_scores()
            self.root.after(100, lambda: messagebox.showinfo("Game Over", "Congratulations! You beat the AI."))
        elif result == AI:
            self.ai_score += 1
            self.status_label.config(text="AI wins! 🤖", fg=DANGER)
            self.update_scores()
            self.root.after(100, lambda: messagebox.showinfo("Game Over", "AI wins. Better luck next time!"))
        else:
            self.draw_score += 1
            self.status_label.config(text="It's a draw! 🤝", fg=GOLD)
            self.update_scores()
            self.root.after(100, lambda: messagebox.showinfo("Game Over", "It's a draw."))

        return True

    def highlight_winning_combo(self, combo):
        for idx in combo:
            self.buttons[idx].config(bg=WIN_BG, fg=WIN_FG)

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def enable_board(self):
        for i, btn in enumerate(self.buttons):
            if self.board[i] == EMPTY:
                btn.config(state="normal")


def main():
    root = tk.Tk()
    app = TicTacToeAI(root)
    root.mainloop()


if __name__ == "__main__":
    main()