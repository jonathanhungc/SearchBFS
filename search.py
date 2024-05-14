# CS 411 - Assignment 3 Starter Code
# Breadth First Search on 15 Puzzle
# Sarit Adhikari
# Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        index = self.tiles.index('0')
        new_state = self.tiles.copy()

        if action == 'U':  # move up
            new_state[index] = new_state[index - 4]
            new_state[index - 4] = '0'
        if action == 'D':  # move down
            new_state[index] = new_state[index + 4]
            new_state[index + 4] = '0'
        if action == 'L':  # move left
            new_state[index] = new_state[index - 1]
            new_state[index - 1] = '0'
        if action == 'R':  # move right
            new_state[index] = new_state[index + 1]
            new_state[index + 1] = '0'

        return Board(new_state)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))


# This class is used to define the breadth first search algorithm
class Search:
    solution = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0"  # String with the solution
    goal_state = Node(Board(solution.split()), None, None)  # Creating a node with the goal state

    # Initialize a frontier (queue), visited set (set) and number of expanded nodes to 0
    def __init__(self):
        self.frontier = deque()
        self.visited = set()
        self.expanded_nodes = 0
        self.memory_bytes = 0

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []   # List for children
        index = parent_node.state.tiles.index('0')  # Find index of blank tile

        if index == 0:  # upper left corner
            # D, R
            for move in ['D', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 3:  # upper right corner
            # D, L
            for move in ['D', 'L']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 12:  # lower left corner
            # U, R
            for move in ['U', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 15:  # lower right corner
            # U, L
            for move in ['U', 'L']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 1 or index == 2:  # upper side (no corner)
            # D, L, R
            for move in ['D', 'L', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 13 or index == 14:  # lower side (no corner)
            # U, L, R
            for move in ['U', 'L', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 4 or index == 8:  # rightmost side (no corner)
            # U, D, R
            for move in ['U', 'D', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 7 or index == 11:  # leftmost side (no corner)
            # U, D, L
            for move in ['U', 'D', 'L']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))
        if index == 5 or index == 6 or index == 9 or index == 10:  # positions in the middle
            # U, D, L, R
            for move in ['U', 'D', 'L', 'R']:
                children.append(Node(parent_node.state.execute_action(move), parent_node, move))

        return children  # return list with children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        current_node = node
        while current_node.parent is not None:  # Loop until reaching root node
            # print(current_node)
            path.append(current_node.action)
            current_node = current_node.parent

        return path[::-1]  # Since we are going from child to root node, reverse list to have path from root to child

    # This function runs breadth first search from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        start_time = time.time()  # start time of the algorithm

        # check initial node to check for goal
        if self.goal_test(root_node):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return self.find_path(root_node), self.expanded_nodes, elapsed_time, self.memory_bytes

        self.frontier.append(root_node)  # add node to frontier
        self.visited.add(root_node)  # add node to visited nodes

        if sys.getsizeof(self.frontier) + sys.getsizeof(self.visited) > self.memory_bytes:
            self.memory_bytes = sys.getsizeof(self.frontier) + sys.getsizeof(self.visited)

        # loop while frontier is not empty
        while len(self.frontier) > 0:

            current_node = self.frontier.popleft()  # pop first element in queue
            self.expanded_nodes += 1

            # loop through the children (or possible moves) of the current node
            for child in self.get_children(current_node):
                if self.goal_test(child):
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return self.find_path(child), self.expanded_nodes, elapsed_time, self.memory_bytes

                # check if child is in visited set
                if child not in self.visited:
                    self.visited.add(child)
                    self.frontier.append(child)
                    if sys.getsizeof(self.frontier) + sys.getsizeof(self.visited) > self.memory_bytes:
                        self.memory_bytes = self.memory_bytes + sys.getsizeof(self.frontier) + sys.getsizeof(self.visited)

        return None

    # Check if the current tiles are the goal state
    def goal_test(self, cur_tiles):
        return cur_tiles == self.goal_state

    # Solves the puzzle by taking the initial configuration of the board, and performing the breadth first search
    # algorithm. It reports the path (or moves) made, the number of expanded nodes, the time taken and the memory
    # used by the algorithm.
    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)


# Testing the algorithm locally
if __name__ == '__main__':
    agent = Search()
    agent.solve("1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15")
