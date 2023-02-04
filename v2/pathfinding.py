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

class Runtime:
    def __init__(self):
        self.run = True

class Field:
    def __init__(self, size, startNodePos, endNodePos, obstacles = []):
        self.grid = self.initGrid(size)
        self.startNode = startNodePos # coords of the endNode
        self.endNode = endNodePos # coords of the startNode
        self.obstacles = obstacles # [] list of the positions 
        self.correctNodes = []

    def initGrid(self, size):
        grid = []
        for i in range(size):
            arr = []
            for j in range(size):
                arr.append(0)
            grid.append(arr)
        return grid

    def print(self) -> None:
        for row in self.grid: 
            print(row)

    def extraPrint(self):
        arr = []
        for row in self.grid:
            save = []
            for j in row:
                if type(j) == Node:
                    save.append("node")
                else:
                    save.append("Free")
            arr.append(save)

        for i in arr:
            print(i)

    def __str__(self) -> str:
        return "Size: {}, Items: {}".format(len(self.grid), len(self.grid)**2)

class Node: 
    def __init__(self, x : int, y : int, endNode, origin = [0, 0], prevG = 0):
        # don't know if needed 
        self.x = x
        self.y = y

        # for backtracking later 
        self.origin = origin

        self.g_cost = prevG + self.stepCost()

        self.h_cost = self.get_h_cost(endNode)

        self.f_cost = self.g_cost + self.h_cost

        self.checked = False

    def get_h_cost(self, endNode) -> int:
        """
        calculates the distance of the node to the end node
        without the obstacles
        """

        dist_a = abs(endNode[0] - self.x)
        dist_b = abs(endNode[1] - self.y)
        
        if dist_a < dist_b:
            dist_a, dist_b = dist_b, dist_a

        dist = dist_b * 14 + (dist_a - dist_b) * 10
        
        return dist

    def stepCost(self) -> int:
        if self.x == self.origin[0] or self.y == self.origin[1]:
            return 10
        return 14

    def getValues(self):
        return "x:{} y:{} o:{} g:{} h:{} f:{}".format(self.x, self.y, self.origin, self.g_cost, self.h_cost, self.f_cost)


def getSurrounding(node, field, run) -> list:
    print(f"working on: {node.getValues()}")
    x = node.x
    y = node.y
    
    position = [x, y]
    # dict of the position around the Node valid or not 
    positions_around = [
        [x+1, y+1],
        [x+1, y],
        [x+1, y-1],
        [x, y+1],
        [x, y-1],
        [x-1, y+1],
        [x-1, y],
        [x-1, y-1]
    ]

    # filter to filter the valid positions 
    sortedMap = []

    # checks if the positions are valid 
    for position in positions_around:
        try: 
            if ((position[0] < 0 or position[1] < 0) 
                or (position == field.startNode)
                or (position in field.obstacles)): 
                pass
            # ending machanism ???
            elif position == field.endNode:
                run.run = False
                return [position]
        
            else: sortedMap.append(position)
        
        except IndexError: pass

    return sortedMap

def calcNodes(origin, field, run) -> None:
    
    round = getSurrounding(origin, field, run)
    print(round)

    # ending machanism ??? 

    for i in round:
        print(i)
        pathNode = Node(i[0], i[1], field.endNode, origin = [origin.x, origin.y], prevG = origin.g_cost)
        try:
            if pathNode.g_cost < field.grid[i[0]][i[1]].g_cost:
                field.grid[i[0]][i[1]] = pathNode
                print("nodeChanged")
        except:
            field.grid[i[0]][i[1]] = pathNode
            print("nodeplaced")

def pickNextNode(field) -> list:

    for row in field.grid:
        for i in row:
            if type(i) == Node and not i.checked:
                point = i
                break

    for row in field.grid:
        for i in row:
            if type(i) == Node and i.f_cost < point.f_cost and not i.checked:
                point = i

    return point

def a_star(field) -> None:
    root = tk.Tk()

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    run = Runtime()
    field.extraPrint()
    startNode = Node(field.startNode[0], field.startNode[1], field.endNode, [field.startNode[0], field.startNode[1]], 0) # temp
    startNode.g_cost = 0
    calcNodes(startNode, field, run)
    field.extraPrint()
    
    save = ""

    while run.run:
        time.sleep(0.5)
        placeCycle(canvas, field)
        currentNode = pickNextNode(field)
        calcNodes(currentNode, field, run)
        currentNode.checked = True
        field.extraPrint()
        save = currentNode

    backTrack(field, save)
    placeCycle(canvas, field)

    root.mainloop()

    # backtrack()

def placeCycle(canvas, field) -> None:
    # start and finish placement

    for widget in canvas.winfo_children():
        widget.destroy()

    startBlock = tk.Canvas(canvas, bg="#3aeb34", height=50, width=50)
    startBlock.place(x=field.startNode[0] * 50, y = field.startNode[1] * 50)

    endBlock = tk.Canvas(canvas, bg="#eb3434", height=50, width=50)
    endBlock.place(x=field.endNode[0] * 50, y = field.endNode[1] * 50)

    for row in field.grid:
        for i in row:
            if type(i) == Node:
                text = f"g: {i.g_cost}\n h: {i.h_cost}\n f: {i.f_cost}"
                pathBlock = tk.Canvas(canvas, bg="#aeeb34", height=50, width=50)
                label = tk.Label(pathBlock, text=text)
                label.pack()
                pathBlock.place(x=i.x * 50, y = i.y * 50)

    for i in field.obstacles:
        obstacle = tk.Canvas(canvas, bg="#000000", height=50, width=50)
        obstacle.place(x=field.i[0] * 50, y = field.i[1] * 50)

    for i in field.correctNodes:
        obstacle = tk.Canvas(canvas, bg="#9803fc", height=50, width=50)
        obstacle.place(x=field.i[0] * 50, y = field.i[1] * 50)

    canvas.update()

def backTrack(field, node):
    while type(field.grid[node.origin[0]][node.origin[1]]) != Node:
        field.correctNodes.append([node.origin[0]][node.origin[1]])
        node = node.origin


def main():
    field = Field(5, startNodePos = [0, 0], endNodePos = [4, 4])
    
    field.print()
     
    a_star(field)


if __name__ == '__main__':
    main()


"""
backtrack 
obstacle show
"""