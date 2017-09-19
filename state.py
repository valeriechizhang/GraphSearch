#!/usr/bin/python

import sys

class State:

    def __init__(self, x_pos, y_pos):
        self.curr_x = x_pos
        self.curr_y = y_pos
        self.moves_so_far = []
        self.cost_so_far = 0
        self.ascore = 0

    def __str__ (self):
        state_str = "Pos=(%d, %d) " % (self.curr_x, self.curr_y)
        state_str += "Moves=%s " % self.moves_so_far
        #state_str += "Moves=[\'" + '\', \''.join(self.moves_so_far) + '\'] '
        #state_str += "Number of moves: %d " % len(self.moves_so_far)
        state_str += "Cost=%d"% self.cost_so_far
        #state_str += " Ascore=%d " % self.ascore
        #state_str += "Length: %s" % len(self.moves_so_far)
        return state_str

