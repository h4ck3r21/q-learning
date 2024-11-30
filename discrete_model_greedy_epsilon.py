from collections import Counter
from typing import List, Tuple
import matplotlib.pyplot as plt 
import random

import numpy

class Discrete_Model:
    q_table: List[List[float]] = []
    past_state_action_reward: List[Tuple[int]] = []
    discount_factor: float 
    learning_rate: float 
    epsilon: float 
    last_state_action: Tuple[int] = None 

    def __init__(self, action_size: int, state_size: int, discount_factor: float = 0.5, learning_rate: float = 0.1, epsilon: float = 0.1):
        self.q_table = [[0] * action_size for _ in range(state_size)]
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        
    def update_table(self, reward: float, state: int):
        #iterative Bellman equation
        self.q_table[self.last_state_action[0]][self.last_state_action[1]] = (1 - self.learning_rate)*(self.q_table[self.last_state_action[0]][self.last_state_action[1]]) + self.learning_rate*(reward + self.discount_factor * max(self.q_table[state]))

    def make_action(self, state: int) -> int:
        p = random.random()
        if p < self.epsilon:
            return random.choice(range(len(self.q_table[state])))
        else:
            x = max(range(len(self.q_table[state])), key=self.q_table[state].__getitem__)
            return x



    def time_step(self, state: int, reward: float = 0) -> int:
        if self.last_state_action is not None:
            self.update_table(reward, state)
        action = self.make_action(state)
        self.last_state_action = (state, action)
        return action


if __name__ == "__main__":
    actions = []
    m = Discrete_Model(2,2, learning_rate=0.1, epsilon=0.1, discount_factor=0.5)
    a = m.time_step(0)
    for i in range(1000):
        if a == 1:
            a = m.time_step(1, -1)
        if a == 0:
            a = m.time_step(0, 1)
        actions.append(a)
    cumulative_average = numpy.cumsum(actions) / (numpy.arange(1000) + 1)
    plt.plot(cumulative_average) 
    plt.show()
