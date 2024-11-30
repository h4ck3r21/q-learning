from abc import ABC, abstractmethod
import json
import random
from threading import Thread

import numpy

from merge_weights import merge_weights
from noughts_and_crosses import Board
from discrete_model_greedy_epsilon import Discrete_Model as Model

class Player(ABC):
    @abstractmethod
    def get_turn(self, board, error):
        pass

    @abstractmethod
    def win(self):
        pass
    
    @abstractmethod
    def lose(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass

class HumanPlayer(Player):
    def get_turn(self, board, error):
        print("Board: ")
        print("\n".join([str(x) for x in board.board]))
        return tuple([int(x) for x in input("place: ").split(", ")])
    
    def win(self):
        print("You win")
    
    def lose(self):
        print("You lose")
    
    def draw(self):
        print("Draw")

class AIPlayer(Player):
    def __init__(self, model):
        self.model = model

    def get_turn(self, board, error):
        #print(board.state)
        if error:
            return POSITIONS[self.model.time_step(reward=ERROR_REWARD, state=board.state)]
        else:
            return POSITIONS[self.model.time_step(reward=TURN_REWARD, state=board.state)]
    
    def win(self):
        self.model.update_table(reward=WIN_REWARD, state=0)
    
    def lose(self):
        self.model.update_table(reward=LOSE_REWARD, state=0)
    
    def draw(self):
        self.model.update_table(reward=DRAW_REWARD, state=0)

class RandomPlayer(Player):
    def get_turn(self, board, error):
        return random.choice(POSITIONS)

    def win(self):
        pass
    
    def lose(self):
        pass
    
    def draw(self):
        pass

end_flag = True
WIN_REWARD = 10
LOSE_REWARD = -20
ERROR_REWARD = -10
DRAW_REWARD = 0
TURN_REWARD = 0
POSITIONS = []
for x in range(3):
    for y in range(3):
        POSITIONS.append((x,y))

def training_thread(model1: Model, model2: Model, N=100000):
    positions = []
    for x in range(3):
        for y in range(3):
            positions.append((x,y))

    i = 0
    while end_flag:
        #resp = []
        #for _ in range(N):
        """if not end_flag:
            return"""
        print(f"epoch: {i}", end="\r")
        generic_game(AIPlayer(model1), AIPlayer(model2))
        #generic_game(AIPlayer(model1), RandomPlayer())
        #generic_game(RandomPlayer(), AIPlayer(model1))
        #model2.q_table = model1.q_table
        i += 1
        """resp.append(ans)

        cumulative_average = numpy.cumsum(resp) / (numpy.arange(N) + 1) 
        print()
        print(cumulative_average[-1])"""
        if i % N == 0:
            with open("onx_weights.txt", "w") as fp:
                merge_weights(model1.q_table, model2.q_table)
                json.dump(model1.q_table, fp)

def generic_game(p1: Player, p2: Player):
    board = Board()
    positions = []
    for x in range(3):
        for y in range(3):
            positions.append((x,y))
    ans = 0

    for i in range(5):
        p = p1.get_turn(board, False)
        ans = board.place(p)
        while ans == -1:
            p = p1.get_turn(board, True)
            ans = board.place(p)
        #if type(p1) == AIPlayer and type(p2) == AIPlayer: p2.model = p1.model
        if ans == 2:
            p1.win()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p2.model = p1.model
            p2.lose()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p1.model = p2.model
            return board
        elif ans == 3:
            p1.draw()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p2.model = p1.model
            p2.draw()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p1.model = p2.model
            return board


        p = p2.get_turn(board, False)
        ans = board.place(p)
        while ans == -1:
            p = p2.get_turn(board, True)
            ans = board.place(p)
        #if type(p1) == AIPlayer and type(p2) == AIPlayer: p1.model = p2.model

        if ans == 1:
            p1.lose()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p2.model = p1.model
            p2.win()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p1.model = p2.model
            return board
        elif ans == 3:
            p1.draw()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p2.model = p1.model
            p2.draw()
            #if type(p1) == AIPlayer and type(p2) == AIPlayer: p1.model = p2.model
            return board
    raise Exception("Something went wrong")
    
if __name__ == "__main__":
    model1 = Model(9, 19683, discount_factor=0.9, learning_rate=0.5)
    model2 = Model(9, 19683, discount_factor=0.9, learning_rate=0.5)
    try:
        with open("onx_weights.txt", "r") as fp:
            model1.q_table = json.load(fp)
            model2.q_table = model1.q_table
    except:
        print("weights cannot be uploaded")


    #training code
    if input("action: ") == "train":
        t = Thread(target=training_thread, args=[model1, model2])
        t.daemon = False
        t.start()

        print("Press Enter to End")
        input()
        with open("onx_weights.txt", "w") as fp:
            json.dump(model1.q_table, fp)
        print("end of training")
        end_flag = False
    else:
        model1.epsilon = 0.0001
        board = generic_game(AIPlayer(model1), HumanPlayer())
        print("Board: ")
        print("\n".join([str(x) for x in board.board]))
        with open("onx_weights.txt", "w") as fp:
            json.dump(model1.q_table, fp)
        
