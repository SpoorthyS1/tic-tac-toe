import prog1

# Initialize game - you play as 'X', AI is 'O' with hard difficulty
game = prog1.create_game(human_symbol='X', ai_difficulty='hard')

# Game loop
while True:
    # Display current board
    game['print_board']()
    
    # Get current state
    state = game['get_state']()
    
    # Check if game is over
    if state['game_over']:
        if state['winner']:
            print(f"Game over! Winner: {state['winner']}")
        else:
            print("Game over! It's a draw!")
        break
        
    # Get user input for next move
    try:
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter column (0-2): "))
        
        # Make the move
        result = game['make_move'](row, col)
        
        if not result['success']:
            print(f"Invalid move: {result['message']}")
    except ValueError:
        print("Please enter valid numbers for row and column")

# Final board state
game['print_board']()