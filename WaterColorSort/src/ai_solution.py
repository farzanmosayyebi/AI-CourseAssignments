from queue import PriorityQueue

class GameSolution:
    """
        A class for solving the Water Sort game and finding solutions(normal, optimal).

        Attributes:
            ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
            moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
            solution_found (bool): True if a solution is found, False otherwise.

        Methods:
            solve(self, current_state):
                Find a solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

            optimal_solve(self, current_state):
                Find an optimal solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """
    def __init__(self, game):
        """
            Initialize a GameSolution instance.
            Args:
                game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.

    def solve(self, current_state):
        """
            Find a solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find a solution to the Water Sort game by iteratively exploring
            different moves and configurations starting from the current state.
        """

        solution = False
        ColorOnTop = -1

        if (self.ws_game.check_victory(current_state)):
            self.solution_found = True
            return

        for bottle1 in range(self.tube_numbers):
            if len(current_state[bottle1]) == 0:
                pass
            
            for bottle2 in range(self.tube_numbers):
                if bottle1 == bottle2 or len(current_state[bottle2]) >= self.ws_game.NColorInTube:
                    pass

                if (self.ws_game.check_victory(current_state)):
                    self.solution_found = True
                    return


                if len(current_state[bottle1]) == 0:
                    break

                solution = False

                if (len(current_state[bottle2]) > 0):
                    ColorOnTop = current_state[bottle2][-1]
                else:
                    ColorOnTop = current_state[bottle1][-1]

                if ColorOnTop == current_state[bottle1][-1]:
                        
                    NewState = self.pour(current_state, bottle1, bottle2)
                    tmp = tuple(map(tuple, NewState))

                    if (tmp not in self.visited_tubes):
                    
                        self.moves.append((bottle1, bottle2))
                        self.visited_tubes.add(tmp)
                        solution = True
                        self.solve(NewState)

                    if self.solution_found:
                        return
                        
        if not solution and self.moves:
            self.moves.pop()



    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
        """

        Frontier = PriorityQueue()
        start = (current_state, [])
        Frontier.put((self.heuristic(current_state) + 0, start)) # tuple(f = g + h, (state, moves))
        gValues = {tuple(map(tuple, current_state)) : 0}
        ColorOnTop = -1

        while (not Frontier.empty()):

            (fValue, (state, moves)) = Frontier.get()
            StateTuple = tuple(map(tuple, state))    
            gValue = gValues[StateTuple]     
               
            if (self.ws_game.check_victory(state)):
                self.solution_found = True
                self.moves = self.moves + moves
                return
            
            self.visited_tubes.add(StateTuple)

            for bottle1 in range (self.tube_numbers):
                if not state[bottle1]:
                    pass
            
                for bottle2 in range (self.tube_numbers):
                    if bottle1 == bottle2:
                        pass

                    if len(state[bottle1]) == 0:
                        break

                    if (len(state[bottle2]) > 0):
                        ColorOnTop = state[bottle2][-1]
                    else:
                        ColorOnTop = state[bottle1][-1]    

                    if ColorOnTop == state[bottle1][-1] and len(state[bottle2]) < self.ws_game.NColorInTube:
                            
                        NewState = self.pour(state, bottle1, bottle2)
                        tmp = tuple(map(tuple, NewState))

                        if (tmp not in self.visited_tubes):
                            moves.append((bottle1, bottle2))
                            gValue = gValue + 1
                            hValue = self.heuristic(NewState)
                            Frontier.put((hValue + gValue, (NewState, moves)))
                            gValues[tmp] = gValue

    # heuristic 1
    ##########################################
    # def heuristic(self, current_state):
    #     h = 0
    #     for bottle in current_state:
    #         h += len(set(bottle))
    #     return h
    ##########################################

    # heuristic 2
    ##########################################
    def heuristic(self, current_state):
        h = 0
        for bottle in current_state:
            if self.IsComplete(bottle):
                h += 1
        return h
    
    def IsComplete(self, bottle):
        for i in range(1, len(bottle)):
            if bottle[i] != bottle[i - 1]:
                return False
        return True
    ##########################################

    def pour(self, State, bottle1, bottle2):
        if (len(State[bottle1]) == 0):
            return State

        length = 0
        ColorToMove = State[bottle1][-1]

        for i in range(len(State[bottle1])):
            if (State[bottle1][-1 - i] != ColorToMove):
                break
            length += 1

        ColorOnTop = -1

        if (len(State[bottle2]) == 0):
            ColorOnTop = ColorToMove
        else:
            ColorOnTop = State[bottle2][-1]

        if (ColorOnTop != ColorToMove):
            return State

        for j in range(length):
            if (len(State[bottle2]) >= self.ws_game.NColorInTube):
                break
            tmp = State[bottle1].pop()
            State[bottle2].append(tmp)
        
        return State


