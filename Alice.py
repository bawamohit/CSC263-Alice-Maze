"""CSC263 PS3: Alice Mazes

=== Module Description ===
This module contains the implementation of an algorithm that solves a given
alice maze represented by the txt file passed as a command line argument.
"""
import sys
from typing import List, Tuple, Optional

TOP = '0'
TOP_RIGHT = '1'
RIGHT = '2'
BOTTOM_RIGHT = '3'
BOTTOM = '4'
BOTTOM_LEFT = '5'
LEFT = '6'
TOP_LEFT = '7'


def build_graph(maze_file: str) -> Tuple[int, List[str], List[List[str]]]:
    """Opens maze_file and reads the contents to store data required to solve
    the maze. This function returns three things:
        1. The dimension (side length) of the maze
        2. A list of arrow colors
        3. A modified adjacency list such as each sublist contains directions
        instead of edges
    """
    arrow_colors = []
    adjacency_list = []
    dimension = 0

    file = open(maze_file, 'r')                     # Opens the file for reading
    for line in file:
        line_values = line.split(' ')     # Splits the line with space delimiter
        for value in line_values:            # Loops over each chunk in the line
            edges = []
            for character in value:     # Loops over each character in the chunk
                if character.isalpha():
                    arrow_colors.append(character)    # Letters represent colors
                elif character.isdigit():
                    edges.append(character)       # Numbers represent directions
            adjacency_list.append(edges)       # Store sublist in adjacency list
        dimension = dimension + 1            # increment dimension once per line
    file.close()

    return dimension, arrow_colors, adjacency_list


def is_valid_edge(position: int, d: str, step_size: int,
                  dim: int) -> bool:
    """A constant time function that determines if there is a vertex step_size
    distance from position in the direction d. Returns true if such a vertex
    exists and false if this edge leads off the maze.
    """
    # Calculates the row of the square at the given position. The first row is
    # at position 0
    row = position // dim
    # Calculates the column of the square at the given position
    col = position % dim

    if row - step_size < 0:         # moving step_size units up is out of bounds
        if d == TOP or d == TOP_RIGHT or d == TOP_LEFT:
            return False       # any direction with upwards component is invalid

    if row + step_size >= dim:   # moving step_size units right is out of bounds
        if d == BOTTOM or d == BOTTOM_RIGHT or d == BOTTOM_LEFT:
            return False    # any direction with rightwards component is invalid

    if col + step_size >= dim:    # moving step_size units down is out of bounds
        if d == RIGHT or d == BOTTOM_RIGHT or d == TOP_RIGHT:
            return False     # any direction with downwards component is invalid

    if col - step_size < 0:       # moving step_size units left is out of bounds
        if d == LEFT or d == BOTTOM_LEFT or d == TOP_LEFT:
            return False     # any direction with leftwards component is invalid

    return True


def find_position(position: int, d: str, step_size: int, dim: int) -> int:
    """A constant time function that returns the position of a vertex
    step_size distance from position in the direction d. This function assumes
    that the requested new position is valid (not out of bounds).
    """
    if d == TOP:
        return position - step_size * dim
    elif d == TOP_RIGHT:
        return position - step_size * (dim - 1)
    elif d == RIGHT:
        return position + step_size
    elif d == BOTTOM_RIGHT:
        return position + step_size * (dim + 1)
    elif d == BOTTOM:
        return position + step_size * dim
    elif d == BOTTOM_LEFT:
        return position + step_size * (dim - 1)
    elif d == LEFT:
        return position - step_size
    elif d == TOP_LEFT:
        return position - step_size * (dim + 1)


def search_maze(dim: int, arr_colors: List[str], adj_list: List[List[str]]) \
        -> Optional[Tuple[int, int, int, List[List[int]]]]:
    """Uses modified breadth first search algorithm to solve the Alice Maze
     of size dim x dim specified by arrow_colors and adjacency_list
    """
    # Stores the most recent distance associated with a square
    # As BFS executes, this is guaranteed to be the minimum distance
    distances = []

    # This is a 2d array such that was_visited[square][step_size - 1] represents
    # in binary if square was visited at this step_size.
    was_visited = []

    # Another 2d array such that parents[square][step_size - 1] gives the parent
    # of this square and the parent's step_size at the time.
    parents = []

    for i in range(dim * dim):                     # For each square in the maze
        distances.append(None)     # In this implementation, None means infinity
        was_visited.append([])
        parents.append([])
        for j in range(dim - 1):            # For every possible valid step_size
            # Initialize every square for all possible step_size to be unvisited
            was_visited[i].append(0)
            # Initialize every square for all possible step_size to be orphans
            parents[i].append(None)

        if arr_colors[i] == 'S':         # Save the location of the start square
            s = i

    was_visited[s][0] = 1      # Stores that s was visited when step_count was 1
    distances[s] = 0         # Stores the distance from the start to itself as 0

    queue = [(s, 1)]
    # In this algorithm, a square is represented by an index such that
    # 0 <= index < total number of squares
    # But since a square can be visited multiple times, a vertex is defined
    # using two values: an index and a step_size

    while len(queue) != 0:       # This is equivalent to the isEmpty() operation
        item = queue.pop(0)                        # Pop an element of the queue
        u = item[0]                                    # u is the current square
        step_size = item[1]                        # Store the current step_size

        if arr_colors[u] == 'R':                              # u has red arrows
            new_step_size = step_size + 1                   # Increase step_size
        elif arr_colors[u] == 'Y':                         # u has yellow arrows
            new_step_size = step_size - 1                   # Decrease step_size
        else:                                               # u has black arrows
            new_step_size = step_size                  # Keep previous step_size

        if 0 < new_step_size < dim:          # If the current step_size is valid
            # For every direction at square u
            for direction in adj_list[u]:
                # Check if step_size units in direction is valid
                if is_valid_edge(u, direction, new_step_size, dim):
                    # Calculate the resulting position
                    v = find_position(u, direction, new_step_size, dim)

                    # If new square was not visited for the current step_size
                    # and it is not a blank square
                    if was_visited[v][new_step_size - 1] == 0 and \
                            arr_colors[v] != 'W':
                        # Set that it was visited
                        was_visited[v][new_step_size - 1] = 1
                        # Set the distance appropriately
                        distances[v] = distances[u] + 1
                        # Set the parent
                        parents[v][new_step_size - 1] = (u, step_size)

                        # If the new square is the goal, we immediately return
                        # because BFS guarantees that the minimum path was found
                        if arr_colors[v] == 'G':
                            # We only require the distance to the goal, the
                            # index of the goal and the final step size and
                            # the list of parents to we can get the full path
                            return distances[v], v, new_step_size, parents

                        # append the new vertex to the queue so it can be
                        # fully explored later
                        queue.append((v, new_step_size))

    # If we get here, the algorithm did not find a path to the goal
    return None


if __name__ == "__main__":
    graph = build_graph(sys.argv[1])                       # Parse the text file
    result = search_maze(graph[0], graph[1], graph[2])    # Run search algorithm

    if result is None:
        print("No solution found")
    else:
        steps = result[0]                # the number of steps to solve the maze
        final_vertex = result[1]                         # the index of the goal
        final_step_size = result[2]    # the step_size when the goal was reached
        tree = result[3]                # the 2d array representation of parents

        print("The Alice Maze was solved in " + str(steps) + " steps.")

        sequence = [final_vertex]       # Create new stack and push final vertex

        # Previous vertex is the parent of final_vertex
        previous_vertex = tree[final_vertex][final_step_size - 1]
        # Walk backwards to the top of the tree until the start is reached
        while previous_vertex is not None:
            sequence.insert(0, previous_vertex[0])  # push onto the stack
            previous_vertex = tree[previous_vertex[0]][previous_vertex[1] - 1]

        print("Sequence of vertices: ")
        print(sequence)
