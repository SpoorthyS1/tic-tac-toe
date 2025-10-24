import prog1

# Example 1: Interactive console gameplay
# Play as 'X' against a hard difficulty AI
prog1.play_game(human_symbol='X', ai_difficulty='hard')

# Example 2: Programmatic API usage
# Create a game instance where you're 'O' and AI is 'X' with easy difficulty
game = prog1.create_game(human_symbol='O', ai_difficulty='easy')

# Get the current game state
state = game['get_state']()
print("Initial board state:")
game['print_board']()

# Make a move (row 0, column 0 - top left corner)
result = game['make_move'](0, 0)
print(f"Move result: {result['success']}")

# Print the board after your move (and AI's response)
game['print_board']()

# Check if the game is over
state = game['get_state']()
if state['game_over']:
    if state['winner']:
        print(f"Game over! Winner: {state['winner']}")
    else:
        print("Game over! It's a draw!")

# Reset the game to start over
game['reset']()
print("Game reset!")
game['print_board']()