#!/usr/bin/python

import environment
import state
import sys

class Search:
    def __init__(self, initial_state, env):
        self.state = initial_state
        self.env = env
        self.frontier = []
        self.visited = []
        self.frontier.append(initial_state)


    def search(self):
        solution = None
        while len(self.frontier) > 0:
            # pop the last state (with the lowest ascore) from the frontier
            # insert it intot the visited list
            pop_state = self.frontier.pop()
            self.visited.append(pop_state)

            # check if the state is goal state
            if self.env.is_goal(pop_state):
                solution = pop_state
                break;

            # if the state is not the goal state
            # we expand the state and general a list of states
            # that can be reached by moving from the current state
            next_moves = self.env.find_moves(pop_state)
            for m in next_moves:
                move = self.make_move(pop_state, m)
                if (self.env.remain_energy(move)):
                    self.insert_frontier(move)

        return solution, self.frontier, self.visited


    def insert_frontier(self, state):
        # if the state's position has been visited
        # we do not insert the state
        for v in self.visited:
            if state.curr_x == v.curr_x and state.curr_y == v.curr_y:
                return

        # if the frontier is empty, just insert the state
        if len(self.frontier) == 0:
            self.frontier.append(state)
            return

        # if another state with the same position is alreay in the frontier
        # remove the one with the higher ascore
        for f in self.frontier:
            if state.curr_x == f.curr_x and state.curr_y == f.curr_y:
                # if the new state has lower ascore
                # we remove the state that's already in the frontier
                # and we will insert the new state later
                if state.ascore < f.ascore:
                    self.frontier.remove(f)
                    break
                # if both have the same ascore
                # or if the new state has higher ascore
                # we do not insert the new state
                else:
                    return

        # insert the state in a way to make sure that
        # the states in the frontier are ordered in descending ascore
        for i in range(0, len(self.frontier)):
            curr = self.frontier[i]
            if curr.ascore > state.ascore:
                # if reach the end of the frontier, just insert
                if i == len(self.frontier) - 1:
                    self.frontier.append(state)
                    return
                continue
            elif curr.ascore <= state.ascore:
                self.frontier.insert(i, state)
                return


    # create a new state based on the state that is coming from
    # and the indended move direction
    def make_move(self, from_state, move):
        new_state = state.State(from_state.curr_x, from_state.curr_y)
        new_state.moves_so_far = from_state.moves_so_far[:]
        if move == 'N':
            new_state.curr_y += 1
        elif move == 'E':
            new_state.curr_x += 1
        elif move == 'S':
            new_state.curr_y -= 1
        elif move == 'W':
            new_state.curr_x -= 1

        new_state.cost_so_far = from_state.cost_so_far + self.cost(from_state, new_state)
        new_state.moves_so_far.append(move)
        new_state.ascore = self.ascore(new_state)
        return new_state


    # generate the cost moving from one state to another
    def cost(self, old_state, new_state):
        cost = 1
        ele_old = self.env.elevations[old_state.curr_y][old_state.curr_x]
        ele_new = self.env.elevations[new_state.curr_y][new_state.curr_x]
        if (ele_old < ele_new):
            cost += (ele_new - ele_old) ** 2
        elif (ele_old > ele_new):
            cost += ele_old - ele_new
        return cost


    # heuristic value based on pre-determined instructions
    def heuristic(self, state):
        h = abs(self.env.end_x - state.curr_x) + abs(self.env.end_y - state.curr_y)
        h = h + abs(self.env.elevations[self.env.end_y][self.env.end_x]
             - self.env.elevations[state.curr_y][state.curr_x])
        return h


    # A* = h(x) + c(x)
    def ascore(self, state):
        return self.heuristic(state) + state.cost_so_far













