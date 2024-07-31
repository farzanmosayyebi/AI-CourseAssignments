import numpy as np

import game_functions as gf


def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.


    ############################## Monotonicity ######################################
    
    BestMonotonicity = -np.inf
    CurrentMonotonicity = int

    for move in range(0, 3):
        
        NonZeroTiles = np.nonzero(board)
        length = len(NonZeroTiles[0])
        CurrentMonotonicity = 0

        for row in range(1, length):
            if (NonZeroTiles[0][row] != NonZeroTiles[0][row - 1]):
                continue
            if (board[NonZeroTiles[0][row]][NonZeroTiles[1][row]] >= board[NonZeroTiles[0][row - 1]][NonZeroTiles[1][row - 1]]):
                CurrentMonotonicity += 1
                  
        for col in range(length):
            for idx in range(col + 1, length):
                if (NonZeroTiles[1][col] == NonZeroTiles[1][idx]):
                    if (board[NonZeroTiles[0][col]][NonZeroTiles[1][col]] >= board[NonZeroTiles[0][idx]][NonZeroTiles[1][idx]]):
                        CurrentMonotonicity += 1
                    break        

        BestMonotonicity = max(BestMonotonicity, CurrentMonotonicity)
        board = np.rot90(board, -1) # rotate the array 90 degrees in the clockwise direction 

    ####################################################################################
    ########################## Distance from the nearest corner ########################

    TotalDist = 0 # sum of (distance from the nearest corner) * (Tile Value) over all tiles
    NonZeroTiles = np.nonzero(board)

    for idx in range(len(NonZeroTiles[0])):
        if (NonZeroTiles[0][idx] < gf.CELL_COUNT // 2):
            i = NonZeroTiles[0][idx]
        else:
            i = gf.CELL_COUNT - NonZeroTiles[0][idx]
        if (NonZeroTiles[1][idx] < gf.CELL_COUNT // 2):
            j = NonZeroTiles[1][idx]
        else:
            j = gf.CELL_COUNT - NonZeroTiles[1][idx]
        TotalDist += ((i + j) * board[NonZeroTiles[0][idx]][NonZeroTiles[1][idx]])

    ####################################################################################
    ################################ Smoothness ########################################
    
    NonZeroTiles = np.nonzero(board)
    TotalDiff = 0 # total difference of all adjacent tiles
    length = len(NonZeroTiles[0])

    for row in range(1, length):
        if (NonZeroTiles[0][row] != NonZeroTiles[0][row - 1]):
            continue
        TotalDiff += abs(board[NonZeroTiles[0][row]][NonZeroTiles[1][row]] - board[NonZeroTiles[0][row - 1]][NonZeroTiles[1][row - 1]])
                  

    for col in range(length):
        for idx in range(col + 1, length):
            if (NonZeroTiles[1][col] == NonZeroTiles[1][idx]):
                TotalDiff += abs(board[NonZeroTiles[0][col]][NonZeroTiles[1][col]] - board[NonZeroTiles[0][idx]][NonZeroTiles[1][idx]])
                break      
                
    ####################################################################################

    W_smoothness = 10 # weight for "Smoothness" feature
    W_dist = 10 # weight for "Distance from the nearest corner" feature
    W_monotonicity = 2048 # weight for "Monotonicity" feature

    features = [BestMonotonicity, TotalDiff, TotalDist]
    weights = [W_monotonicity, W_smoothness, W_dist]

    TotalValue = 0

    for i in range(len(features)):
        TotalValue += (weights[i] * features[i])

    return TotalValue

    #raise NotImplementedError("Evaluation function not implemented yet.")



# def Rotate90Degrees_CW(board: np.ndarray):
#     len = gf.CELL_COUNT
#     for i in range(len // 2):
#         for j in range(i, len - i - 1):
#             temp = board[i][j]
#             board[i][j] = board[len - 1 - j][i]
#             board[len - 1 - j][i] = board[len - 1 - i][len - 1 - j]
#             board[len - 1 - i][len - 1 - j] = board[j][len - 1 - i]
#             board[j][len - 1 - i] = temp
