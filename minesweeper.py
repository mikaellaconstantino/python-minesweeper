def generate_mines():
    import itertools
    import random as rand
    from string import ascii_uppercase
    return [ascii_uppercase[a] + str(b+1) for a, b in rand.sample(list(itertools.product(range(7), repeat=2)), k=8)]

def create_board(rows, cols, mines):
    column_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
    board = []                                  # Placeholder to ng grid. :)).
    for _ in range (rows):                      # Sa bawat row, magkakaroon ng " . " sa bawat col; Basically, malalagyan ng dots yung column.
        row = []                                # Placeholder ng dots.
        for _ in range (cols):                  # So, here, sa bawat column magkakaroon dot sa row na katapat niya.
            row.append('.')                     # Code para sa paglalagay ng dots.
        board.append(row)                       # Lalagay natin yung row (na may dot) sa board.

    defuser_mine = mines[-1]                # Pinakadulo ng generated mine ang kukunin natin as defuser.
    mines = mines[:-1]                      # Basically, mawawala na sa list ng mines natin yung pinakadulo, since sinet na natin siya as defuser.

    for mine in mines:  # Placing of Mines
        col = column_mapping[mine[0].upper()]   # Convert column letter to index (A-G to 0-6).
        row = int(mine[1:]) - 1                 # Convert natin tong row numerical string to integer; 1:, kasi nagstart siya from A1 not A0. (1-7 to 0-6).
        board[row][col] = '!'                   # kapag nakakuha na ng cell, ilalagay natin as ! yung bomb.

    # Place the defuser on the board
    col = column_mapping[defuser_mine[0].upper()]  # Place the defuser using the column mapping.
    row = int(defuser_mine[1:]) - 1
    board[row][col] = 'D'                          # 'D' to represent the defuser on the board (won't be visible unless prompted)

    return board

def print_board(board):
    rows = len(board)       # number of list, board has 7 lists
    cols = len(board[0])    # number of columns, each list may 7 elements inside

    print('===== M I N E S W E E P E R =====')

    col_labels = '   ' + ' A   B   C   D   E   F   G'  # Print A-G
    print(' ' + col_labels)                            # space lang para maayos tignan

    for i in range(rows):
        row_str = '[' + str(i + 1) + '] '              # Print the rows [1] to [7]
        row_str += '   '.join(str(cell) if cell != 'D' else 'D' for cell in board[i]) # print the dots or else the D
        print(' ' + row_str)

    total_mines = 7                                     # Count the mines 8-1 because of Defuser
    flagged_mines = 0                                   # Placeholder para sa flagged mines
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '?' or board[r][c]=='*':  # kapag yung cell == ?, meaning flagged siya, mababawasan yung naka-print na mines left sa game area
                flagged_mines += 1

    mines_left = total_mines - flagged_mines            # math eq to print
    print('\nMines Left:' + str(mines_left) + '\n')     # final print indicating the number of mines left


def count_adjacent_mines(board, row, col):  # In this function it will count the adjacent or nearby mines 
    rows, cols = len(board), len(board[0])  # Same sa taas
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # Creates a list of tuples repre the 8 adjacent sides surrounding a particular cell (cell is at (0,0)/origin) 
    count = 0                                                                           # Dito, initialize natin count var as 0 para masstore niya yung number ng flagged na katabi
    for dr, dc in directions:                                                           # dr will take the row value from the tuple, dc will take the column value from tups.
        r = row + dr            # Here, cinacalculate natin yung row number in a certain direction by adding dr to input row
        c = col + dc            # Same here, but sa column naman
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == '!':                      # Chinecheck nito if within yung calculated r and c sa bounds ng grid and if yung particular cells na chinecheck ay mine (indicated as "!")
            count += 1          # if na-satisfy, will increment.

    return count 

def count_flagged_neighbors(board, revealed, row, col): 
    rows, cols = len(board), len(board[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] 
    count = 0 
    for dr, dc in directions: 
        r = row + dr 
        c = col + dc 
        if 0 <= r < rows and 0 <= c < cols and revealed[r][c] == '?':  
            count += 1

    return count

def play_game(rows, cols, mines):   
    column_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
    defuser = mines[-1] 
    board = create_board(rows, cols, mines)
    revealed = []                                       # Placeholder 
    for _ in range (rows):                              # Sa bawat row, magkakaroon ng " . " sa bawat col; Basically, malalagyan ng dots yung column
        row = []                                        # Placeholder ng dots.
        for _ in range (cols):                          # So, here, sa bawat column magkakaroon dot sa row na katapat niya.
            row.append('.')                             # Code para sa paglalagay ng dots.
        revealed.append(row)                            # Lalagay natin yung row (na may dot) sa board.
    
    mines_count = len(mines) - 1                        # defuser yung isa so, (num of mines - 1)
    game_over = False                                   # Starting with the assumption na hindi pa nag-eend yung game
    win = False                                         # Hindi pa nananalo yung user
    defuser_acquired = False                            # and hindi pa nakukuha yung defuser
    defuser_acquired_once = False                       # para isang beses lang mag print ng status kung nakakuha ng defuser
                                                    # Basically, used to to track the progress, magcchange ang vals nito habang naglalaro yung user, and magrreflect yung update sa game state
    def count_revealed_cells():
        return sum(1 for row in revealed for cell in row if cell != '.' and cell !='?')     # bibilangin yung nareveal na cells para malaman kung nanalo
    revealed_cells = set()                                                                  
    def count_notdot_cells():
        return sum(1 for row in revealed for cell in row if cell == '.' )                   # bibilangin yung nareveal na cells na hindi dots para malaman kung nanalo
    while not game_over and not win:
       # var =count_notdot_cells()
       # print(var)                             # So hangga't hindi pa tapos yung game: lahat ito mangyayari
        print_board(revealed)                                                   # start and every other move
        if defuser_acquired_once:                                               
            print('You found the defuser at ' + str(defuser) + ' You can now use it as a power-up:\n')  
            defuser_acquired_once = False 

        print("Controls:")                                                      # Displayed from start to every other move
        print("[O] Open a cell")
        print("[F] Flag/Unflag a cell")
        print("[Ctrl + C] Exit Game")
        if defuser_acquired:
            print("[D] Use Defuser")                                            # Kapag merong defuser, magpprint na to sa terminal

        valid_action = False                                                    # Katulad sa taas

        while not valid_action:                                                        # babalik pag di true, iccheck if withing the given choices lang yung iniinput
            action = input().upper()                                                   # gagawing uppercase lahat ng letter or input
            if action == 'O' or action == 'F' or (action == 'D' and defuser_acquired): # pwede lang if may defuser
                valid_action = True                                                    # If nasatisfy, will be changed into true
            else:
                print("Invalid input. Please choose 'O' to open a cell, 'F' to flag/unflag a cell.")

        print("Enter a coordinate ([A-G][1-7]) (e.g 'B3'):")
        valid_input = False                                                                 # Checks if within the coordinate lang ng board yung ineenter

        while not valid_input:
            input_str = input()
            if len(input_str) == 2 and input_str[0].isalpha() and input_str[1].isdigit():   # Condtions: 2 strings, yung una dapat Letter and yung pangalawa dapat number
                
                col_str = input_str[0].upper()              # first index of input will rep col and transformed into uppercase
                row_str = input_str[1]                      # second index of input will rep the row
                if col_str in column_mapping:
                    col = column_mapping[col_str]           # will convert A-G to 0-6
                    row = int(row_str) - 1                  # will convert numerical string 1-7 to 0-6
                    if 0 <= row < rows and 0 <= col < cols: # checks if the input is within the boundary of the given num of grid
                        valid_input = True
                    else:
                        print("Out of bounds. Please enter a valid coordinate.")
                else:
                    print("Out of bounds. Please enter a valid coordinate.")
                 #para maging 0-6
            else:
                print("Invalid input. Please enter a coordinate as 'B3' or 'F4'.")  #trapping nung inputs

        if action == 'O':                                                        # If ang choice ay mag-open ng cell
            
            if (row, col) in revealed_cells:                                     # will loop through each revealed cell on board                                                           
                flagged = count_flagged_neighbors(board, revealed, row, col)     # for each cell, will count the num of neighbor flag cells
                if revealed[row][col] == str(flagged):                           # if num of flagged neighbors matches the revealed val at that particular cell,
                    count = count_adjacent_mines(board, row, col)                # it will count the num of adjacent mines
                    revealed[row][col] = str(count)                              # here, maguupdate yung revealed value at that cell to show the num of adj mines
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # will check the 8 adjacents cells
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols:                       # check if it is within the num of rows and cols
                            if revealed[nr][nc] == '.':                             # if any neighbors is unrevealed, reveal it
                                if board[nr][nc] == '!':                            # if mine yung nareveal, 
                                    game_over = True                                # talo na and game will end
                                    revealed[nr][nc] = '!'                          # then ippakita na other mines
                                elif board[nr][nc] == 'D':                          # if defuser is acquired the ff will happen
                                     defuser_acquired = True
                                     defuser_acquired_once = True
                                     count = count_adjacent_mines(board, nr, nc)
                                     revealed[nr][nc] = str(count)
                                else:
                                    count = count_adjacent_mines(board, nr, nc)
                                    revealed[nr][nc] = str(count)
                            revealed_cells.add((nr, nc))
               
                
            elif revealed[row][col] == '.':                             
                
                if board[row][col] == '!':                              # ilalabas yung mine
                    game_over = True                                    # talo na
                    revealed[row][col] = '!'                            # ilabas yung mine
                elif board[row][col] == 'D':                            # ilalabas yung defuser
                    defuser_acquired_once = True                        # true
                    defuser_acquired = True   
                    count = count_adjacent_mines(board, row, col)       # imbes na D icount yung mga katabing mines
                    revealed[row][col] = str(count)
                    revealed_cells.add((row, col))                         # same logic sa pagbukas number pa din
                else:
                    count = count_adjacent_mines(board, row, col)       # execute the if not Defuser or Mine eto yung mga numbers 
                    revealed[row][col] = str(count)                     # print yung number                                               
                    revealed_cells.add((row, col))                      # iadd natin para malaman kung naopen na ba yung cells at hindi

            # Check for win condition
            
            if count_revealed_cells() >= rows * cols - mines_count:
                if count_notdot_cells() == 0:
                         win = True
            
        elif action == 'D':      # Defuse Action Only Visible when Defuser is acquired
                        
            if board[row][col] == '!':
                revealed[row][col] = '*'
            else:
              count = count_adjacent_mines(board, row, col) 
              revealed[row][col] = str(count)
              revealed_cells.add((row, col))
            	  #gagawing asterisk yung cell
            directions1 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions1:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols: 
                        if board[nr][nc] == '!':                        # lahat ng may mines gagawing asterisk
                            revealed[nr][nc] = '*'
            defuser_acquired = False                                    # ibabalik sa false kasi isang beses lang siya ginamit

 
         
        else:                               # flagging and unflagging of cells
            if revealed[row][col] == '.':   # pag tuldok gagawing ?
                revealed[row][col] = '?'
            elif revealed[row][col] == '?': # pag ? gagawing tuldok
                revealed[row][col] = '.'


    print_board(revealed)
    
    if game_over: # print ng game result
        print("Game Over! You hit a mine.")
    elif win:
        print("Congratulations! You won!")
        


rows, cols = 7, 7
mines = generate_mines() # for example (['G1', 'A2', 'A3', 'D5', 'A5', 'A6', 'A7', 'F7'])
play_game(rows, cols, mines)