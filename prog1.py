import time
import random

class TicTacToe:
    def __init__(self):
        # Step 1: Initialize the board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'  # X starts first
    
    def reset(self):
        """Reset the game to initial state"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'

    def print_board(self):
        # Step 2: Print the board
        print("\n  0 1 2")
        for i, row in enumerate(self.board):
            print(f"{i} {' | '.join(row)}")
            if i < 2:
                print("  ---------")
        print()

    def is_draw(self):
        # Check if the game is a draw
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def is_game_over(self, board=None):
        if board is None:
            board = self.board  # Default to the current board state
        # Check rows
        for row in board:
            if row.count(row[0]) == len(row) and row[0] != ' ':
                return row[0]
        # Check columns
        for col in zip(*board):
            if col.count(col[0]) == len(col) and col[0] != ' ':
                return col[0]
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        return False

    def make_move(self, row, col):
        """Make a move on the board"""
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        
        if self.board[row][col] != ' ':
            return False
            
        self.board[row][col] = self.player
        # Switch player
        self.player = 'O' if self.player == 'X' else 'X'
        return True

    def dfs(self, board, depth, player):
        # Step 5: DFS logic to choose the best move
        winner = self.is_game_over(board)
        if winner:
            if winner == 'X':  # AI wins
                return {'score': 1}
            else:  # Human wins
                return {'score': -1}
        elif self.is_draw():
            return {'score': 0}  # Draw

        best = {'score': -float('inf')} if player == 'X' else {'score': float('inf')}
        symbol = 'X' if player == 'X' else 'O'

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = symbol
                    score = self.dfs(board, depth + 1, 'O' if player == 'X' else 'X')
                    board[i][j] = ' '
                    score['row'] = i
                    score['col'] = j

                    if player == 'X':  # Maximize for AI
                        if score['score'] > best['score']:
                            best = score
                    else:  # Minimize for opponent
                        if score['score'] < best['score']:
                            best = score
        return best

    def get_available_moves(self):
        """Return list of available moves as (row, col) tuples"""
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == ' ':
                    moves.append((r, c))
        return moves
        
    def get_board_state(self):
        """Return a copy of the current board state"""
        return [row[:] for row in self.board]
        
    def get_current_player(self):
        """Return the current player symbol"""
        return self.player

    def play(self):
        # Original game loop
        while True:
            self.print_board()
            winner = self.is_game_over()
            if winner or self.is_draw():
                print("Game Over.")
                if self.is_draw():
                    print("It's a draw!")
                else:
                    print(f"Player {winner} wins!")
                break

            if self.player == 'X':
                print("AI is making a move...")
                best_move = self.dfs(self.board, 0, 'X')
                self.board[best_move['row']][best_move['col']] = 'X'
                self.player = 'O'  # Switch to next player
            else:
                # Step 4: Accept keyboard input for 'O'
                while True:
                    try:
                        row = int(input("Enter the row number (0-2): "))
                        col = int(input("Enter the column number (0-2): "))
                        if self.board[row][col] == ' ':
                            self.board[row][col] = 'O'
                            self.player = 'X'  # Switch to next player
                            break
                        else:
                            print("Invalid move. Try again.")
                    except (ValueError, IndexError):
                        print("Invalid input. Please enter numbers between 0 and 2.")


class AIAgent:
    """AI agent for playing Tic Tac Toe with adjustable difficulty."""
    
    def __init__(self, difficulty='hard', player_symbol='O'):
        self.difficulty = difficulty.lower()
        self.symbol = player_symbol
        self.opponent_symbol = 'O' if player_symbol == 'X' else 'X'
    
    def get_move(self, game):
        """Get the AI's next move based on difficulty level"""
        if self.difficulty == 'easy':
            return self._get_random_move(game)
        elif self.difficulty == 'medium':
            return self._get_medium_move(game)
        else:  # hard - use DFS/minimax
            return self._get_best_move_dfs(game)
    
    def _get_random_move(self, game):
        """Choose a random valid move"""
        available_moves = game.get_available_moves()
        return random.choice(available_moves)
    
    def _get_medium_move(self, game):
        """Try to win or block opponent, or random move"""
        # This is a simplified medium difficulty
        # First try a random move 50% of the time
        if random.random() < 0.5:
            return self._get_random_move(game)
        # Otherwise use the best move (hard difficulty)
        return self._get_best_move_dfs(game)
    
    def _get_best_move_dfs(self, game):
        """Use the game's DFS algorithm to get the best move"""
        best_move = game.dfs(game.board, 0, self.symbol)
        return (best_move['row'], best_move['col'])


def play_game(human_symbol='O', ai_difficulty='hard'):
    """
    Play a complete interactive Tic Tac Toe game in the console.
    
    Args:
        human_symbol: 'X' or 'O' (X goes first)
        ai_difficulty: 'easy', 'medium', or 'hard'
    """
    game = TicTacToe()
    ai_symbol = 'O' if human_symbol == 'X' else 'X'
    ai = AIAgent(ai_difficulty, ai_symbol)
    
    print("Welcome to Tic Tac Toe!")
    print(f"You are {human_symbol}, AI is {ai_symbol}")
    print("Enter moves as row column (e.g., '1 2')")
    
    while True:
        game.print_board()
        winner = game.is_game_over()
        
        if winner or game.is_draw():
            if winner:
                if winner == human_symbol:
                    print("Congratulations! You won!")
                else:
                    print("AI won! Better luck next time.")
            else:
                print("It's a draw!")
            break
        
        current_player = game.get_current_player()
        
        if current_player == human_symbol:
            # Human's turn
            valid_move = False
            while not valid_move:
                try:
                    move_input = input(f"Your move ({human_symbol}): ")
                    row, col = map(int, move_input.split())
                    valid_move = game.make_move(row, col)
                    if not valid_move:
                        print("Invalid move! Try again.")
                except (ValueError, IndexError):
                    print("Please enter row and column as two numbers (0-2).")
        else:
            # AI's turn
            print(f"AI ({ai_symbol}) is thinking...")
            time.sleep(0.5)  # Add a small delay for better UX
            move = ai.get_move(game)
            game.make_move(*move)
            print(f"AI placed at: {move[0]} {move[1]}")
    
    # Show final board state
    game.print_board()


def create_game(human_symbol='X', ai_difficulty='medium'):
    """
    Create a new game instance for programmatic use.
    
    Returns:
        dict: Game interface with methods for interacting with the game
    """
    game = TicTacToe()
    ai_symbol = 'O' if human_symbol == 'X' else 'X'
    ai = AIAgent(ai_difficulty, ai_symbol)
    
    def make_human_move(row, col):
        """Make a move for the human player and get updated game state."""
        if game.is_game_over() or game.is_draw():
            return {
                'success': False,
                'message': "Game is already over",
                'state': get_game_state()
            }
        
        if game.get_current_player() != human_symbol:
            return {
                'success': False,
                'message': "Not your turn",
                'state': get_game_state()
            }
        
        success = game.make_move(row, col)
        if not success:
            return {
                'success': False,
                'message': "Invalid move",
                'state': get_game_state()
            }
        
        # If game not over and AI's turn, make AI move
        winner = game.is_game_over()
        if not (winner or game.is_draw()) and game.get_current_player() == ai_symbol:
            ai_move = ai.get_move(game)
            game.make_move(*ai_move)
        
        return {
            'success': True,
            'message': "Move successful",
            'state': get_game_state()
        }
    
    def get_game_state():
        """Get the current state of the game."""
        winner = game.is_game_over()
        game_over = winner or game.is_draw()
        
        return {
            'board': game.get_board_state(),
            'current_player': game.get_current_player(),
            'game_over': game_over,
            'winner': winner if winner else None,
            'is_draw': game.is_draw(),
            'available_moves': game.get_available_moves()
        }
    
    def reset_game():
        """Reset the game to initial state."""
        game.reset()
        
        # If AI goes first, make its move
        if game.get_current_player() == ai_symbol:
            ai_move = ai.get_move(game)
            game.make_move(*ai_move)
            
        return {
            'success': True,
            'message': "Game reset",
            'state': get_game_state()
        }
    
    # If AI goes first, make its move now
    if game.get_current_player() == ai_symbol:
        ai_move = ai.get_move(game)
        game.make_move(*ai_move)
    
    # Return the game interface
    return {
        'make_move': make_human_move,
        'get_state': get_game_state,
        'reset': reset_game,
        'print_board': game.print_board
    }


# For direct usage as a script
if __name__ == "__main__":
    game = TicTacToe()
    game.play()