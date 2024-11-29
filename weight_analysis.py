import json


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

s = 17809
print(l[s])
print(state_to_board(s))