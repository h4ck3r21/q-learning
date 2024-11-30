import json

from noughts_and_crosses import Board
from discrete_model_greedy_epsilon import Discrete_Model as Model


try:
    with open("onx_weights.txt", "r") as fp:
        l = json.load(fp)
except:
    print("weights cannot be uploaded")

def state_to_board(state):
    board = [[0] * 3 for _ in range(3)]
    for x in range(3):
        for y in range(3):
            board[x][y] = state % 3
            state -= state % 3
            state /= 3
    return board

s = 5731
print(l[s])
print(state_to_board(s))
print("----")

b = Board()
b.board = [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
b.update_state()
print(l[b.state])
m = Model(9, 19683)
m.q_table = l
print(m.make_action(b.state))
