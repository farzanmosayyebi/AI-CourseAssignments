import numpy as np

import evaluation
import game_functions as gf


class MCTS:
    def __init__(self, board, mode='ucb'):
        self.C_CONSTANT = 2  # You may change this parameter to scale the exploration term in the UCB formula.
        self.SD_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.TM_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.SCALER_PARAM = 200  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_SD_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_TM_SCALE_PARAM = 5  # You may change this parameter to scale the depth to which the agent searches.
        self.UCB_SCALER_PARAM = 300  # You may change this parameter to scale the depth to which the agent searches.
        self.board = board
        self.mode = mode

    def get_search_params(self, move_number: int) -> (int, int):
        """
        Returns the depth to which the agent should search for the given move number.
        ...
        :type move_number: int
        :param move_number: The current move number.
        :return: The depth to which the agent should search for the given move number.
        """
        # TODO: Complete get_search_params function to return the depth to which the agent should search for the given move number.
        # Hint: You may want to use the self.SD_SCALE_PARAM, self.SL_SCALE_PARAM, and self.SCALER_PARAM parameters.
        # Hint: You may want to use the self.UCB_SPM_SCALE_PARAM, self.UCB_SL_SCALE_PARAM, and self.UCB_SCALER_PARAM parameters.
        # Hint: You may want to use the self.mode parameter to check which mode the agent is on.

        search_depth = 1
        total_moves = 1

        ######
        #
        #code#
        #
        ######

        return search_depth, total_moves
        
        # raise NotImplementedError("Get search params not implemented yet.")

    def ai_move(self, board, move_number):
        search_depth, total_moves = self.get_search_params(move_number)
        if self.mode == 'ucb':
            best_move = self.mcts_v2(board, total_moves * 4, search_depth)
        else:
            best_move = self.mcts_v0(board, total_moves, search_depth)
        return best_move

    @staticmethod
    def simulate_move(board: np.ndarray, search_depth: int) -> float:
        """
        Returns the score of the given board state.
        :param board: The board state for which the score is to be calculated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: The score of the given board state.
        """
        # TODO: Complete simulate_move function to simulate a move and return the score of the given board state.
        # Hint: You may want to use the gf.random_move function to simulate a random move.
        # Hint: You may want to use the evaluation.evaluate_state function to score a board.
        # Hint: You may want to use the move_made returned from the gf.random_move function to check if a move was made.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.

        TotalScore = 0
        BoardCopy = np.copy(board)
        move_made = False

        for i in range(search_depth):
        
            while(not move_made):
                BoardCopy, move_made, score = gf.random_move(BoardCopy)

            gf.add_new_tile(BoardCopy)
            score += evaluation.evaluate_state(BoardCopy)
            TotalScore += score

        return TotalScore
        
        # raise NotImplementedError("Simulate move not implemented yet.")
        

    def ucb(self, moves: list, total_visits: int) -> np.ndarray:
        """
        Returns the UCB scores for the given moves.
        :param moves: The moves for which the UCB scores are to be calculated.
        :param total_visits: The total number of visits for all moves.
        :return: The UCB scores for the given moves.
        """
        # TODO: Complete ucb function to return the UCB scores for the given moves.
        # Hint: You may want to use the self.C_CONSTANT parameter to scale the exploration term in the UCB formula.
        # Hint: You may want to use np.inf to represent infinity.
        # Hint: You may want to use np.sqrt to calculate the square root of a number.
        # Hint: You may want to use np.log to calculate the natural logarithm of a number.
        
        UCB1_values = []
        
        for move in moves:
            action, utility, num_of_simulations = move
            
            if (num_of_simulations == 0):
                UCB1 = -np.inf
            else:
                UCB1 = (utility / num_of_simulations) + (self.C_CONSTANT * np.sqrt(np.log(total_visits) / num_of_simulations))
            
            UCB1_values.append((action, UCB1))

        return UCB1_values

        # raise NotImplementedError("UCB not implemented yet.")

    def mcts_v0(self, board: np.ndarray, total_moves: int, search_depth: int):
        """
        Returns the best move for the given board state.
        ...
        :type search_depth: int
        :type total_moves: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param total_moves: The total number of moves to be simulated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: Returns the best move for the given board state.
        """
        # TODO: Complete mcts_v0 function to return the best move for the given board state.
        # Hint: You may want to use the gf.get_moves function to get all possible moves.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may want to use the self.simulate_move function to simulate a move.
        # Hint: You may want to use the np.argmax function to get the index of the maximum value in an array.
        # Hint: You may want to use the np.zeros function to create an array of zeros.
        # Hint: You may want to use the np.copy function to create a copy of a numpy array.

        moves = gf.get_moves()
        scores = np.zeros(len(moves))

        for move in range(len(moves)):

            BoardCopy = np.copy(board)
            for sim in range(total_moves):
                scores[move] += self.simulate_move(BoardCopy, search_depth)
            
            scores[move] /= total_moves

        return moves[np.argmax(scores)]

        # raise NotImplementedError("MCTS v0 not implemented yet.")

    def mcts_v2(self, board, total_moves, search_depth):
        """
        Returns the best move for the given board state.
        ...
        :type search_depth: int
        :type total_moves: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param total_moves: The total number of moves to be simulated.
        :param search_depth: The depth to which the agent should search for the given board state.
        :return: Returns the best move for the given board state.
        """
        # TODO: Complete mcts_v2 function to return the best move for the given board state.
        # Hint: You may want to use the gf.get_moves function to get all possible moves.
        # Hint: You may want to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may want to use the self.simulate_move function to simulate a move.
        # Hint: You may want to use the np.argmax function to get the index of the maximum value in an array.
        # Hint: You may want to use the np.copy function to create a copy of a numpy array.
        # Hint: You may want to use the self.ucb function to get the UCB scores for the given moves.

        moves = gf.get_moves()
        moves_tuples = []
        
        for move in moves:
            BoardCopy = np.copy(board)
            BoardCopy, move_made, score = move(BoardCopy)
            
            if (move_made):
                moves_tuples.append((move, score, total_moves + 1))
                
        BoardCopy = np.copy(board)
        
        ucb_values = self.ucb(moves_tuples, total_moves)
        
        total_score = 0

        max_index = np.argmax(ucb_values)
        action = moves_tuples[max_index]
        BoardCopy, move_made, score = action(BoardCopy)

        for i in range(total_moves):
            total_score += self.simulate_move(BoardCopy, search_depth)
            
        if (move_made):
            total_score += score
            gf.add_new_tile(BoardCopy)
        else:
            total_score -= 50
                
        return action
    
        # raise NotImplementedError("MCTS v2 not implemented yet.")
    