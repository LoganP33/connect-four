import numpy as np 
from random import randrange
import time

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
  board = np.zeros((6, 7))
  return board

#Creates an array history which will stored the column # of each move which can be used to recreate each move of the board at the end.
#The array can be as large as 42 because that is the maximum amound of moves in a game of connect 4. 
#The array is filled with integer 9 because it is an impossible column choice thus it will serve as a stopping point in a while loop when obtaining elements and size
#of the array
def create_history():                   
    history = np.full(42,9)
    return history

#Function used to show user each turn of the game, inputs are two arrays, each representing the order of moves that each player perfomed (columns), gamepiece types and IDs
#The length of the two history_arrays are calculated by incrementing a counter until history_array[counter] equals 9, an impossible move for the user to make,
#thus breaking the loop and setting the length. These two lengths are then added together (total_length) and used to create the combined_history array which will store
#each move stored by the players in alternating order, just as they were placed on the previously played game.
def show_game_history(history_array1, history_array2, gamepiece1, gamepiece2, ID1, ID2):
    last_game_board = create_board() #Creates board which will show the history of the previously played game
    #counter and length variables initializion
    i = 0
    j = 0
    length1 = 0
    length2 = 0
    turn_counter = 0

    #the size of each array is calculated by iterating through each array until a 9 is reached. The lengths of each array are added and stored into the 
    #total_length variable which is used to specify the size of the combined array
    while(history_array1[length1] != 9):
        length1+=1
    while(history_array2[length2] != 9):
        length2+=1
    
    total_length = length1 + length2
    combined_history = np.full(total_length,0)

    #Since player1 always goes first (could change in future builds) length1 will ALWAYS be either >= length2.
    #Using this fact two if statements are used to iterate through the two history arrays which have the columns the players selected
    #These column numbers are stored in the combined array in the order player1 move -> player2 move -> player1 move -> player 2 move ..... ->
    #Until j equals length1 (length1 > length2) or until j is not less than length1 (length1 == length2)
    if(length1 > length2):
        while(j != length1):
            combined_history[i] = history_array1[j]
            if(i+1 != total_length):
                combined_history[i+1] = history_array2[j]
            i+=2
            j+=1
    elif(length1 == length2):
        while(j < length1):
            combined_history[i] = history_array1[j]
            combined_history[i+1] = history_array2[j]
            i+=2
            j+=1
    
    #After the combined_history array has been created, the first move is automatically stored at the first index [0] of the last_game_board and printed for the user
    #The user than can choose to see the next move or exit to menu. If the user choose to continue then they will enter a while loop that executes until they choose
    #to return to main menu or the review ends.
    turn_counter = 0
    col = combined_history[0]
    turn_counter += 1
    row = get_next_open_row(last_game_board, col) 
    drop_gamepiece(last_game_board, row, col, gamepiece1)
    print("\n========================================Turn #" + str(turn_counter) + " Player " + ID1 + "(" + str(gamepiece1) + ")'s turn========================================\n")    
    print_gameboard(last_game_board)
    print("")
    print("1.) Next Move\n2.) Exit to Main Menu")
    history_option = int(input())
    if(history_option == 1):
        k = 1
    else:
        return
    
    #While loop which starts at k=1 since by this point the first move has been added to the board. It will increment until k == total_length which signifies that each move
    #has been reviewed.
    #variable turn_counter is used to display the turn number as well as used to alternate between printing ID1/2 and gamepiece1/2 to the terminal.
    while(k < total_length):
        col = combined_history[k]
        turn_counter += 1
        row = get_next_open_row(last_game_board, col) 
        if(turn_counter %2 == 0):
            drop_gamepiece(last_game_board, row, col, gamepiece2)
            print("\n========================================Turn #" + str(turn_counter) + " Player " + ID2 + "(" + str(gamepiece2) + ")'s turn========================================\n")        
        else:
            drop_gamepiece(last_game_board, row, col, gamepiece1)
            print("\n========================================Turn #" + str(turn_counter) + " Player " + ID1 + "(" + str(gamepiece1) + ")'s turn========================================\n")        
            if(k == total_length - 1):
                break
        print_gameboard(last_game_board)
        print("")
        print("1.) Next Move\n2.) Exit to Main Menu")
        history_option = int(input())
        if(history_option == 1):
            k += 1
        else:
            print("================================================================================")
            return
    
    global confirm_tie
    if(round_count == 43 and winning_move(last_game_board, row, col, gamepiece1) != True and winning_move(last_game_board, row, col, gamepiece2) ):
        confirm_tie = 1
    if(turn_counter %2 == 0 and confirm_tie != 1):
        print(last_game_board)
        print("")
        print("Player " + ID2 + "(" + str(gamepiece2) + ") Wins!\nThe review is finished, please select an option\n\n1.) Review Again\n2.) Return to Main Menu")
    elif(turn_counter %2 != 0 and confirm_tie != 1):
        print(last_game_board)
        print("")
        print("Player " + ID1 + "(" + str(gamepiece1) + ") Wins!\nThe review is finished, please select an option\n\n1.) Review Again\n2.) Return to Main Menu")
    elif(confirm_tie == 1):
        print(last_game_board)
        print("")
        print("The game is a tie!\nThe review is finished, please select an option\n\n1.) Review Again\n2.) Return to Main Menu")
        confirm_tie = 0
    
    end_review_option = int(input())
    if(end_review_option == 1):
        show_game_history(history_array1, history_array2, gamepiece1, gamepiece2, ID1, ID2)
    if(end_review_option == 2):
        print("\n============================================================================================================\n")
        return

#places the gamepiece
def drop_gamepiece(board, row, col, gamepiece): 
    board[row][col] = gamepiece

#checks if the selected colomn is full
def is_valid_location(board, col): 
  if(board[0][col] == 0):
    return True

#Prints the gameboard with visual indicators for each column above
def print_gameboard(board):
    print("  0  1  2  3  4  5  6")
    print("  |  |  |  |  |  |  |")
    print(board)

#Finds the next avaiable row a gamepiece can be placed
def get_next_open_row(board, col):
    r = 0
    while(r in range(ROW_COUNT-1) and board[r][col] == 0): #looks at array from top down
        if(r <= 4 and board[r+1][col] != 0):
            break
        r+=1
    return r  #returns first row = 0

#Checks each possible win condition for
def winning_move(board, r, c, gamepiece):
  #check horizontal locations for win 
   #check below [-][]
    if(r <= 2):
        if (board[r+1][c] == gamepiece and board[r+2][c] == gamepiece and board[r+3][c] == gamepiece):
            return True
    #check left and right [][-] and [][+]
    if (c <= 3):                                                                                            #Checks for: O-X-X-X
        if (board[r][c+1] == gamepiece and board[r][c+2] == gamepiece and board[r][c+3] == gamepiece):
            return True
    if(c >= 2 and c != 6):                                                                                  #Checks for: X-X-O-X
        if (board[r][c-1] == gamepiece and board[r][c-2] == gamepiece and board[r][c+1] == gamepiece):
            return True
    if(c >= 1 and c <= 4):                                                                                  #Checks for: X-O-X-X
        if (board[r][c-1] == gamepiece and board[r][c+1] == gamepiece and board[r][c+2] == gamepiece):
            return True
    if(c >= 3):                                                                                             #Checks for: X-X-X-O
        if (board[r][c-1] == gamepiece and board[r][c-2] == gamepiece and board[r][c-3] == gamepiece):
            return True

    #check upper/lower right/left diagonal    [-][+] and [-][-]
    if(r >= 3 and c <= 3):                                                                                      #Checks for: O/X/X/X
        if (board[r-1][c+1] == gamepiece and board[r-2][c+2] == gamepiece and board[r-3][c+3] == gamepiece):
            return True
    if(r >= 2 and r<= 4 and c <= 4 and c >= 1):                                                                 #Checks for: X/O/X/X
        if (board[r-1][c+1] == gamepiece and board[r-2][c+2] == gamepiece and board[r+1][c-1] == gamepiece):
            return True
    if(r >= 1 and r <= 3 and c <= 5 and c >= 2 ):                                                               #Checks for: X/X/O/X
        if (board[r-1][c+1] == gamepiece and board[r+1][c-1] == gamepiece and board[r+2][c-2] == gamepiece):
            return True
    if(r <= 2 and c >= 3):                                                                                      #Checks for: X/X/X/O
        if (board[r+1][c-1] == gamepiece and board[r+2][c-2] == gamepiece and board[r+3][c-3] == gamepiece):
            return True
    if(r <= 2 and c <= 3):                                                                                      #Checks for: O\X\X\X
        if (board[r+1][c+1] == gamepiece and board[r+2][c+2] == gamepiece and board[r+3][c+3] == gamepiece):
            return True
    if(r <= 3 and r >= 1 and c <= 4 and c >= 1):                                                                #Checks for: X\O\X\X
        if (board[r+1][c+1] == gamepiece and board[r+2][c+2] == gamepiece and board[r-1][c-1] == gamepiece):
            return True
    if(r <= 4 and r >= 2 and c >= 2 and c <= 5):                                                                #Checks for: X\X\O\X
        if (board[r+1][c+1] == gamepiece and board[r-1][c-1] == gamepiece and board[r-2][c-2] == gamepiece):
            return True
    if(r >= 3 and c >= 3):                                                                                      #Checks for: X\X\X\O
        if (board[r-1][c-1] == gamepiece and board[r-2][c-2] == gamepiece and board[r-3][c-3] == gamepiece):
            return True

#This function prompts the user to make a selection on the board and 
def player_move(gamepiece, playerID, history_array):
    print("\n========================================Turn #" + str(round_count) + "========================================\n")
    print_gameboard(board)
    col = int(input ("Player " + playerID + "(" + str(gamepiece) + ")" + " Make your Selection (0-6):"))
    #Used for game history that if round_count has reached 42 and the tie is confirmed print to the screen that the game is a tie

    i = 0
    while(i != 2):                              #Until you get a valid location, continue this loop
        if(is_valid_location(board, col)):
            move = 0
            while(history_array[move] != 9): 
                move+=1
            history_array[move] = col
            row = get_next_open_row(board, col) #Row is assigned based on the next available row in the column
            drop_gamepiece(board, row, col, gamepiece)
            i = 2
        else:
            print("\n======================Invalid move. Please select a column with an open space======================\n")
            print(board)
            col = int(input ("Player " + playerID + "(" + str(gamepiece) + ")" + " Make your Selection (0-6):"))
      
    if winning_move(board, row, col, gamepiece) == True:
        print("\n================================================================================================")
        print("========================================THE GAME IS OVER========================================")
        print("================================================================================================\n")
        print(board)
        print("Player " + playerID + "(" + str(gamepiece) + ")" + " Wins!")
        global game_over
        game_over = 2

    if(round_count == 42 and winning_move(board, row, col, gamepiece) != True):
        print("\n================================================================================================")
        print("========================================THE GAME IS OVER========================================")
        print("================================================================================================\n")
        print(board)
        print("The game is a tie!")
        confirm_tie = 1
        game_over = 2

def computer_move(gamepiece, computerID, computerMode, history_array):
    print("\n========================================Turn #" + str(round_count) + "========================================\n")
    print_gameboard(board)
    print(computerID + "(" + str(gamepiece) + ")" + " Is making a selection...")
    time.sleep(1)
    col = pick_best_move(board, AI_PIECE)

    i = 0
    while(i != 2):                              #Until you get a valid location, continue this loop
        if(is_valid_location(board, col)):
            move = 0
            while(history_array[move] != 9): 
                move+=1
            history_array[move] = col
            row = get_next_open_row(board, col) #Row is assigned based on the next available row in the column
            drop_gamepiece(board, row, col, gamepiece)
            i = 2
        else:
            col = pick_best_move(board, AI_PIECE)     
    
    if winning_move(board, row, col, gamepiece) == True:
            print("\n================================================================================================")
            print("========================================THE GAME IS OVER========================================")
            print("================================================================================================\n")
            print(board)
            print("The Computer(" + str(gamepiece) + ") Wins!")
            global game_over
            game_over = 2

    if(round_count == 42 and winning_move(board, row, col, gamepiece) != True):
            print("\n================================================================================================")
            print("========================================THE GAME IS OVER========================================")
            print("================================================================================================\n")
            print(board)
            print("The game is a tie!")
            confirm_tie = 1
            game_over = 2

####################################################################################################################
###################################################  AI SECTION #################################################### 
####################################################################################################################

## This function creates the score of certain moves
def evaluate_window(window, piece):
    opp_piece = PLAYER_PIECE
    score = 0
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    
    #if AI can get four in a row the score is raised by 100
    if window.count(piece) == 4:
        score += 100
    #if AI can get three in a row the score is raised by 10
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    #if AI can get two in a row the score is raised by 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5
    #if the user can get four in a row the score is decreased by 80
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80

    return score

## This function scores a certain spot based on the current position of the board
def score_position(board, piece):
    score = 0

    #scoring center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    #scoring horizontally
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #scoring vertically
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #scoring positive diagonally
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+1] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    #scoring negative diagonally
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


## This creates an array of all possible valid columns to drop a piece into
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

#This takes the number of the column with the highest score and places a piece in that spot
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_gamepiece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

#######################################################################################################################
#######################################################################################################################
########################################################################################################################

def player_vs_player(history_array1, history_array2):
    global game_over
    game_over = 1
    global round_count
    round_count = 1
    global player1ID
    player1ID = input("Enter a name for player 1: ")
    global player2ID
    player2ID = input("Enter a name for player 2: ")
    global confirm_tie
    confirm_tie = 0
    print("")


    while(game_over != 2):
        player_move(1, player1ID, history_array1)
        round_count +=1
        if(game_over == 2):                 #Need better idea than global variable...
            break
        player_move(2, player2ID, history_array2)
        round_count +=1

#Player vs Computer
def player_vs_computer(histoy_array1, history_array2):
    global game_over
    game_over = 1
    global round_count
    round_count = 1
    global player1ID
    player1ID = input("Enter a name for player 1: ")
    global computer1ID 
    global confirm_tie
    confirm_tie = 0
    computer1ID = "Computer"
    computer_mode = 1               #Computer is easy mode (random moves)

    while(game_over != 2):
        player_move(1, player1ID, history_array1)
        round_count +=1
        if(game_over == 2):                 #Need better idea than global variable...
            break
        computer_move(2, computer1ID, computer_mode, history_array2)
        round_count +=1

#Computer vs Computer
def computer_vs_computer(histoy_array1, history_array2):
    global game_over
    game_over = 1
    global round_count
    round_count = 1
    global computer1ID
    computer1ID = "Computer1"
    global computer2ID 
    computer2ID = "Computer2"
    global confirm_tie
    confirm_tie = 0
    computer1_mode = 1               #Computer is easy mode (random moves)
    computer2_mode = 1

    while(game_over != 2):
        computer_move(1, computer1ID, computer1_mode, history_array1)
        round_count +=1
        if(game_over == 2):                 #Need better idea than global variable...
            break
        computer_move(2, computer2ID, computer2_mode, history_array2)
        round_count +=1

########### Main ###########
end = 0                                    #Variable used to exit program
while(end != 2):
    print("Connect Four Main Menu\n1.) Player Vs. Player\n2.) Player Vs. Computer\n3.) Computer Vs. Computer\n4.) Exit")
    global history_array1
    history_array1 = create_history()
    global history_array2
    history_array2 = create_history()
    #global round count variable which is used to determine whether the game reached the final turn and if it's a tie (42 total rounds)
    mainmenu_option = int(input())

    if(mainmenu_option == 1):
        board = create_board()
        player_vs_player(history_array1, history_array2)
        endgame_option = 0
        while(endgame_option != 3):
            print("\nSelect an Option\n1.) Rematch\n2.) Show Game History\n3.) Return to Main Menu\n")
            endgame_option = int(input())
            if(endgame_option == 1):
                board = create_board()
                history_array1 = create_history()
                history_array2 = create_history()
                player_vs_player(history_array1,history_array2)
            elif(endgame_option == 2):
                show_game_history(history_array1, history_array2, 1, 2, player1ID, player2ID)
                endgame_option = 3

    
    if(mainmenu_option == 2):
        endgame_option = 0
        board = create_board()
        player_vs_computer(history_array1, history_array2)
        while(endgame_option != 3):
            print("\nSelect an Option\n1.) Rematch\n2.) Show Game History\n3.) Return to Main Menu\n")
            endgame_option = int(input())
            if(endgame_option == 1):
                board = create_board()
                player_vs_computer(history_array1, history_array2)
            elif(endgame_option == 2):
                show_game_history(history_array1, history_array2, 1, 2, player1ID, computer1ID)
                endgame_option = 3

    if(mainmenu_option == 3):
        endgame_option = 0
        board = create_board()
        computer_vs_computer(history_array1, history_array2)
        while(endgame_option != 3):
            print("\nSelect an Option\n1.) Rematch\n2.) Show Game History\n3.) Return to Main Menu\n")
            endgame_option = int(input())
            if(endgame_option == 1):
                board = create_board()
                computer_vs_computer(history_array1, history_array2)
            elif(endgame_option == 2):
                show_game_history(history_array1, history_array2, 1, 2, computer1ID, computer2ID)
                endgame_option = 3
        
    if(mainmenu_option == 4):
        print("Program exiting...")
        end = 2