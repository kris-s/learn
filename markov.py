#!/usr/local/bin/python3
from time import sleep
from random import random


class State:
    def __init__(self, name, probabilities):
        self.name = name
        self.probabilities = probabilities


def main():
    chain = [
        State("rain", (0.3, 0.3, 0.4)),
        State("sun", (0.1, 0.8, 0.1)),
        State("overcast", (0.4, 0.1, 0.5))
    ]

    state = 0

    while True:
        state = update(chain, state)
        print("Today's weather is: {}".format(chain[state].name))
        sleep(2)


def update(chain, state):
    choice = random()
    probability_sum = 0.0
    for i, new_state_probability in enumerate(chain[state].probabilities):
        probability_sum += new_state_probability
        if choice < probability_sum:
            return i

if __name__ == '__main__':
    main()
