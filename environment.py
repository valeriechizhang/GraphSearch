#!/usr/bin/python

import state
import sys

class Environment:
    'Map-based environment'

    # Member data
    # elevations: raw data for each position, stored in a list of lists
    #             (each outer list represents a single row)
    # height: number of rows
    # width: number of elements in each row
    # end_x, end_y: location of goal

    def __init__(self, mapfile, energy_budget, end_coords):
        self.elevations = []
        self.height = 0
        self.width = -1
        self.end_x, self.end_y = end_coords
        self.energy_budget = energy_budget
        # Read in the data
        for line in mapfile:
            nextline = [ int(x) for x in line.split() ]
            if self.width == -1:
                self.width = len(nextline)
            elif len(nextline) == 0:
                sys.stderr.write("No data (or parse error) on line %d\n"
                                 % (len(self.elevations) + 1))
                sys.exit(1)
            elif self.width != len(nextline):
                sys.stderr.write("Inconsistent map width in row %d\n"
                                 % (len(self.elevations) + 1))
                sys.stderr.write("Expected %d elements, saw %d\n"
                                 % (self.width, len(nextline)))
                sys.exit(1)
            self.elevations.insert(0, nextline)
        self.height = len(self.elevations)
        if self.end_x == -1:
            self.end_x = self.width - 1
        if self.end_y == -1:
            self.end_y = self.height - 1


    def is_goal(self, state):
        if (state.curr_x == self.end_x and state.curr_y == self.end_y):
            return True
        return False


    def remain_energy(self, state):
        if (self.energy_budget >= state.cost_so_far):
            return True
        return False


    def find_moves(self, state):
        moves = []
        x = state.curr_x
        y = state.curr_y
        if y < self.height - 1:
            moves.append('N')
        if x < self.width - 1:
            moves.append('E')
        if y > 0:
            moves.append('S')
        if x > 0:
            moves.append('W')
        return moves










