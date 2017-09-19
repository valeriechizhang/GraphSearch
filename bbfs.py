#!/usr/bin/python

import environment
import state
import sys
import time

class Search:
    def __init__(self, initial_state, env):
        self.env = env
        self.start_state = initial_state
        self.goal_state = state.State(self.env.end_x, self.env.end_y)
        self.start_frontier = []
        self.start_visited = []
        self.goal_frontier = []
        self.goal_visited = []

        self.start_frontier.append(initial_state)
        self.goal_frontier.append(self.goal_state)


    def search(self):
        solution = None
        frontier = None
        visited = None

        while len(self.start_frontier) > 0 and len(self.goal_frontier) > 0:

            solution = self.check_solution()
            if solution:
                frontier = self.start_frontier + self.goal_frontier
                visited = self.start_visited + self.goal_visited
                break

            if len(self.start_frontier) > 0:
                move_length = len(self.start_frontier[len(self.start_frontier)-1].moves_so_far)
                while (len(self.start_frontier) > 0
                    and len(self.start_frontier[len(self.start_frontier)-1].moves_so_far) == move_length):
                    pop_state = self.start_frontier.pop()
                    self.start_visited.append(pop_state)
                    next_moves = self.env.find_moves(pop_state)
                    for m in next_moves:
                        move = self.make_start_move(pop_state, m)
                        if self.env.remain_energy(move) and not self.check_start_visited(move):
                            self.start_frontier_insert(move)

            solution = self.check_solution()
            if solution:
                frontier = self.start_frontier + self.goal_frontier
                visited = self.start_visited + self.goal_visited
                break

            if len(self.goal_frontier) > 0:
                move_length = len(self.goal_frontier[len(self.goal_frontier)-1].moves_so_far)
                while (len(self.goal_frontier) > 0
                    and len(self.goal_frontier[len(self.goal_frontier)-1].moves_so_far) == move_length):
                    pop_state = self.goal_frontier.pop()
                    self.goal_visited.append(pop_state)
                    next_moves = self.env.find_moves(pop_state)
                    for m in next_moves:
                        move = self.make_goal_move(pop_state, m)
                        if self.env.remain_energy(move) and not self.check_goal_visited(move):
                            self.goal_frontier_insert(move)

        return solution, frontier, visited


    # create a new state based on the state that is coming from
    # and the indended move direction
    def make_start_move(self, from_state, move):
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
        return new_state

    def make_goal_move(self, from_state, move):
        dict = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
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

        new_state.cost_so_far = from_state.cost_so_far + self.cost(new_state, from_state)
        new_state.moves_so_far.insert(0, dict[move])
        return new_state


    def check_start_visited(self, state):
        for v in self.start_visited:
            if v.curr_x == state.curr_x and v.curr_y == state.curr_y:
                return True
        return False


    def check_goal_visited(self, state):
        for v in self.goal_visited:
            if v.curr_x == state.curr_x and v.curr_y == state.curr_y:
                return True
        return False


    def start_frontier_insert(self, state):
        for s in self.start_frontier:
            if s.curr_x == state.curr_x and s.curr_y == state.curr_y:
                if len(s.moves_so_far) > len(state.moves_so_far):
                    self.start_frontier.remove(s);
                elif len(s.moves_so_far) == len(state.moves_so_far):
                    if s.cost_so_far > state.cost_so_far:
                        self.start_frontier.remove(s);
                    else:
                        return
        self.start_frontier.insert(0, state)


    def goal_frontier_insert(self, state):
        for s in self.goal_frontier:
            if s.curr_x == state.curr_x and s.curr_y == state.curr_y:
                if len(s.moves_so_far) > len(state.moves_so_far):
                    self.goal_frontier.remove(s);
                elif len(s.moves_so_far) == len(state.moves_so_far):
                    if s.cost_so_far > state.cost_so_far:
                        self.goal_frontier.remove(s);
                    else:
                        return
        self.goal_frontier.insert(0, state)


    def intersect(self, list_a, list_b):
        intersection = []
        for a in list_a:
            for b in list_b:
                if a.curr_x == b.curr_x and a.curr_y == b.curr_y:
                    new_state = self.combine_state(a, b)
                    if self.env.remain_energy(new_state):
                        intersection.append(new_state)
        return intersection


    def combine_state(self, a, b):
        res = state.State(self.goal_state.curr_x, self.goal_state.curr_y)
        res.moves_so_far = a.moves_so_far + b.moves_so_far
        res.cost_so_far = a.cost_so_far + b.cost_so_far
        return res


    def check_solution(self):
        solution = None
        intersection = self.intersect(self.start_frontier, self.goal_frontier)
        if len(intersection) > 0:
            solution = intersection[0]
            for i in intersection:
                if len(i.moves_so_far) < len(solution.moves_so_far):
                    solution = i
                elif len(i.moves_so_far) == len(solution.moves_so_far):
                    if i.cost_so_far < solution.cost_so_far:
                        solution = i
        return solution


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



