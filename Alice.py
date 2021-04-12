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
    """Opens maze_file and returns an adjacency list representation of a graph,
    where the edges are represented by the constant directions defined above.
    """
    arrow_colors = []
    adjacency_list = []

    file = open(maze_file, 'r')
    for line in file:
        line_values = line.split(' ')
        dimension = 0
        for value in line_values:
            edges = []
            for character in value:
                if character.isalpha():
                    arrow_colors.append(character)
                elif character.isdigit():
                    edges.append(character)
            adjacency_list.append(edges)
            dimension = dimension + 1
    file.close()

    return dimension, arrow_colors, adjacency_list


def is_valid_edge(position: int, d: int, step_size: int,
                  dim: int) -> bool:
    """A constant time function that determines if there is a vertex step_size
    distance from position in the direction d.
    """
    row = position // dim
    col = position % dim

    if row - step_size < 0:
        if d == TOP or d == TOP_RIGHT or d == TOP_LEFT:
            return False

    if row + step_size >= dim:
        if d == BOTTOM or d == BOTTOM_RIGHT or d == BOTTOM_LEFT:
            return False

    if col + step_size >= dim:
        if d == RIGHT or d == BOTTOM_RIGHT or d == TOP_RIGHT:
            return False

    if col - step_size < 0:
        if d == LEFT or d == BOTTOM_LEFT or d == TOP_LEFT:
            return False

    return True


def find_position(position: int, d: int, step_size: int, dim: int) -> int:
    """A constant time function that determines the position of a vertex
    step_size distance from position in the direction d.
    """
    if d == TOP:
        return position - step_size * dim
    if d == TOP_RIGHT:
        return position - step_size * (dim - 1)
    if d == RIGHT:
        return position + step_size
    if d == BOTTOM_RIGHT:
        return position + step_size * (dim + 1)
    if d == BOTTOM:
        return position + step_size * dim
    if d == BOTTOM_LEFT:
        return position + step_size * (dim - 1)
    if d == LEFT:
        return position - step_size
    if d == TOP_LEFT:
        return position - step_size * (dim + 1)


def find_shortest_path(s: int, dim: int, arrow_colors: List[str],
                       adjacency_list: List[List[str]]) \
        -> Optional[Tuple[int, int, List[int]]]:
    """Uses modified breadth first search algorithm to solve the Alice Maze
     of size dim x dim specified by arrow_colors and adjacency_list
    """
    num_vertices = dim * dim

    colors = []
    distances = []
    parents = []

    for i in range(num_vertices):
        colors.append('W')
        distances.append(None)  # In this implementation, None means infinity
        parents.append(None)

        if arrow_colors[i] == 'S':
            s = i

    colors[s] = 'G'
    distances[s] = 0

    queue = [(s, 1)]
    while len(queue) != 0:
        item = queue.pop(0)
        u = item[0]
        step_size = item[1]
        for direction in adjacency_list[u]:
            if is_valid_edge(u, direction, step_size, dim):
                v = find_position(u, direction, step_size, dim)

                if colors[v] == 'W':
                    colors[v] = 'G'
                    distances[v] = distances[u] + 1
                    parents[v] = u

                    if arrow_colors[v] == 'G':
                        return v, distances[v], parents
                    elif arrow_colors[v] == 'R':
                        queue.append((v, step_size + 1))
                    elif arrow_colors[v] == 'Y':
                        queue.append((v, step_size - 1))
                    else:
                        queue.append((v, step_size))
        colors[u] = 'B'

    return None


if __name__ == "__main__":
    print(sys.argv[1])
    graph = build_graph(sys.argv[1])
    print(graph[0])
    print(graph[1])
    print(graph[2])
    result = find_shortest_path(6, graph[0], graph[1], graph[2])
    if result is None:
        print("No solution found")
    else:
        print(result[0])
        print(result[1])
        print(result[2])
