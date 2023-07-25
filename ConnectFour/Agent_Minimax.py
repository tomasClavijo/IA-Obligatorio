from board import Board
from agent import Agent
import random

animation = [
    "[=     ]",
    "[ =    ]",
    "[  =   ]",
    "[   =  ]",
    "[    = ]",
    "[     =]",
    "[    = ]",
    "[   =  ]",
    "[  =   ]",
    "[ =    ]",
]

class AgentMinimax(Agent):
    def __init__(self, player=1):
        super().__init__()
        self.player = player;
        self.other_player = 2;
    def next_action(self, board: Board) -> tuple[int, int]:
        self.idx = 0
        pos, _ = self.minimax(board, self.player,4)
        return pos

    def minimax(self, board: Board, player: int, d : int)-> tuple[tuple[int, int], int]:
        # Animación para que se vea lindo
        print(animation[int(self.idx/300) % len(animation)], end="\r")
        self.idx += 1
        # Fin de animacion

        #TODO: Completar
        actions = board.get_posible_actions()
        random.shuffle(actions)
        #Caso base
        ended = board.is_final()
        if ended or d==0:
            if board.winner == self.player:
                return None, 100
            if board.winner == self.other_player:
                return None, -100
            if board.is_full():
                return None, 0
            else:
                return None, self.heuristic_utility(board)

        #Casos no base
        action_nodes = []

        for action in actions:
            child_node = board.clone()
            child_node.add_tile(action, player)
            action_nodes.append((action, child_node))

        value = float('-inf') if player == 1 else float('inf')
        chosen_action = None  
        
    
        if player != 1: # mini
            for action_node in action_nodes:
                aux_action, aux_value = self.minimax(action_node[1],1, d-1);
                if(aux_value <= value):
                    value = aux_value;
                    chosen_action = action_node[0];
            pass
        else: #max (player == self.player)
            for action_node in action_nodes:
                aux_action, aux_value = self.minimax(action_node[1],2,d-1);
                if(aux_value >= value):
                    value = aux_value;
                    chosen_action = action_node[0];
            pass

        return chosen_action, value
    
    def heuristic_utility(self, board: Board):
        #Contamos cantidad de O´s en el tabler y le restamos la cantidad de X´s
        o_count = 0;
        x_count = 0;
        for column in range(board.heigth):
            for row in range(board.length):
                if board.grid[column][row] == "X":
                    x_count = x_count + 1;
                elif board.grid[column][row] == "O":
                    o_count = o_count + 1;
                
         #Contamos la cantidad de alineaciones de 3 O s que hay, restamos las alineaciones de 3 X s que hay.
        o_aligned = 0;
        x_aligned = 0;
        # Nos fijamos en alineaciones horizontales
        for i in range(board.heigth):
            for j in range(board.length - 3):
                if board.grid[i][j] == "X" and board.grid[i][j+1] == "X" and board.grid[i][j+2] == "X" and board.grid[i][j+3] == "X":
                    x_aligned += 1
                if board.grid[i][j] == "O" and board.grid[i][j+1] == "O" and board.grid[i][j+2] == "O" and board.grid[i][j+3] == "O":
                    o_aligned += 1

        # Nos fijamos en alineaciones verticales 
        for i in range(board.heigth - 3):
            for j in range(board.length):
                if board.grid[i][j] == "X" and board.grid[i+1][j] == "X" and board.grid[i+2][j] == "X" and board.grid[i+3][j] == "X":
                    x_aligned += 1
                if board.grid[i][j] == "O" and board.grid[i+1][j] == "O" and board.grid[i+2][j] == "O" and board.grid[i+3][j] == "O":
                    o_aligned += 1

        # Nos fijamos en alineaciones diagonales
        for i in range(board.heigth - 3):
            for j in range(board.length - 3):
                if board.grid[i][j] == "X" and board.grid[i+1][j+1] == "X" and board.grid[i+2][j+2] == "X" and board.grid[i+3][j+3] == "X":
                    x_aligned += 1
                if board.grid[i][j] == "O" and board.grid[i+1][j+1] == "O" and board.grid[i+2][j+2] == "O" and board.grid[i+3][j+3] == "O":
                    o_aligned += 1


        # Nos fijamos en alineaciones diagonales (inclinacion negativa)
        for i in range(3, board.heigth):
            for j in range(board.length - 3):
                if board.grid[i][j] == "X" and board.grid[i-1][j+1] == "X" and board.grid[i-2][j+2] == "X" and board.grid[i-3][j+3] == "X":
                    x_aligned += 1
                if board.grid[i][j] == "O" and board.grid[i-1][j+1] == "O" and board.grid[i-2][j+2] == "O" and board.grid[i-3][j+3] == "O":
                    o_aligned += 1
        return 300*(o_count - x_count) + 300*(o_aligned - x_aligned);







