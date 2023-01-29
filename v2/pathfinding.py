import numpy as np
import tkinter as tk
import time

"""
pseudo code


node class
    checked bool
    g_cost int 
        origin g_cost + step cost
    h_cost int
        distance to end node (function is ok)
    f_cost int 
        g_cost + h_cost
    origin prev Node
    type ? string ? 
    x int pos in the array
    y int pos in the array 


origin node, start node
    -> generate new ones
        ->pick the best from the new ?
            -check if tested
        -> repeat
    -> get end with end node

backtrack
    take last node wich found endnode 
    and get with the origins where is came from 
        path in an new array i guess ? 

"""

class Grid:
    def __init__(self, size, startNodePos, endNodePos, obstacles = []):
        self.grid = [[0] * size] * size
        self.endNode = startNodePos # coords of the endNode
        self.startNode = endNodePos # coords of the startNode
        self.obstacles = obstacles # [] list of the positions 

    def print(self) -> None:
        for row in self.grid: 
            print(row)

    def __str__(self) -> str:
        return "Size: {}, Items: {}".format(len(self.grid), len(self.grid)**2)

class Node: 
    def __init__(self, x : int, y : int, origin = [0, 0]):
        # don't know if needed
        self.x = x
        self.y = y

        # for backtracking later 
        self.origin = origin

        self.g_cost = self.get_g_cost()

        self.h_cost = self.get_h_cost(endNode)

    def get_g_cost(self):
        return self.origin.g_cost + self.stepCost()

    def get_h_cost(self, endNode) -> int:
        """
        calculates the distance of the node to the end node
        without the obstacles
        """

        dist_a = abs(endNode.x - self.x)
        dist_b = abs(endNode.y - self.y)
        
        if dist_a < dist_b:
            dist_a, dist_b = dist_b, dist_a

        dist = dist_b * 14 + (dist_a - dist_b) * 10
        
        return dist

    def stepCost(self, coordOne, coordTwo):
        if self.x == coordTwo[0] or self.y == coordOne[1]:
            return 10
        return 14

def main():
    """
    def function
    
    """

    pass



if __name__ == '__main__':
    main()