# GraphSearch
The program demonstrates an A* graph search algorithm and a bidirectional breadth-first search algorithm.

The environment is comprised of a rectangular grid, and each position has an non-negative integer indicates its elevation.
The agent's mission is to find the route from the starting position to the destination position with the lowest cost. In addition, the agent will have an “energy budget” to use, which is the maximum amount of energy the agent can use to
reach the goal location. The cost of moving from one location to another is a fixed cost of 1, plus the cost of elevation change. For an uphill move,
it’s the change in elevation squared. For a downhill move, it’s the change in elevation. The heuristic value is the Manhattan distance to the goal plus the change in
elevation between the current location and the goal.


### How to run:
Run individual tests: ./main.py <astar or bbfs>.py tests/<map-name>.map --energy --start-x --start-y --end-x --end-y

Run all tests: ./run_tests.sh tests


### Reference:
Santa Clara University COEN266 Artificial Intelligence
