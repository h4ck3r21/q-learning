import random
from typing import Tuple


class Board:
    board = [[0] * 3 for _ in range(3)]
    state = 0
    next_tile = 2
    # 0 = empty, 19682 = game filled with 2's => 19683 states
    def __init__(self):
        self.board = [[0] * 3 for _ in range(3)]

    def update_state(self):
        i = 0
        state = 0
        for row in self.board:
            for tile in row:
                state += 3**i * tile
                i += 1
        self.state = state
    
    def place(self, position: Tuple[int, int]) -> int:
        if self.board[position[0]][position[1]] == 0:
            tile = self.next_tile
            if tile == 1:
                self.next_tile = 2
            else:
                self.next_tile = 1
            self.board[position[0]][position[1]] = tile
            self.update_state()
            return self.check_end(position)
        else:
            return -1
        
    def check_end(self, position: Tuple[int, int]) -> int:
        # 0 = no end, 1 = tile1 wins, 2 = tile2 wins
        LINES = [
            0b000000111,
            0b000111000,
            0b111000000,
            0b100100100,
            0b010010010,
            0b001001001,
            0b100010001,
            0b001010100
        ]
        i = 0
        bin_state = 0
        for row in self.board:
            for tile in row:
                bin_state += 2**i * (tile == self.board[position[0]][position[1]])
                i += 1
        for line in LINES:
            if line & bin_state == line:
                return self.board[position[0]][position[1]]
            
        if bin(bin_state).count("1") == 5:
            return 3
        else:
            return 0


if __name__ == "__main__":
    b = Board()
    positions = []
    for x in range(3):
        for y in range(3):
            positions.append((x,y))
    ans = 0
    while ans == 0 or ans == -1:
        p = random.choice(positions)
        print(p)
        ans = b.place(p)
        print("\n".join([str(x) for x in b.board]))
        print(ans)
