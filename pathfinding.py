# algorithm name "A*"
import numpy as np 
import time
import tkinter as tk

class Grid: 
    def __init__(self, size):
        self.grid = self.initGrid(size)

    def initGrid(self, size) -> np.array:
        grid = []

        for i in range(size):
            row = []
            for j in range(size):
                row.append(Node(i, j))       
            grid.append(row)

        return np.array(grid)

    def positionNode(self, *args) -> None:
        for node in args:
            self.grid[node.pos_x][node.pos_y] = node
        

    def print(self) -> None:
        for i in self.grid:
            outString = ""
            for j in i:
                outString += "{} | ".format(j.getValues())
            print(outString)
    def __str__(self) -> None:
        return "Size: {}, Items: {}".format(len(self.grid), len(self.grid)**2)

class Node: 
    def __init__(self, pos_x : int, pos_y : int,):
        self.pos_x = pos_x
        self.pos_y = pos_y
        
    def __str__(self) -> str:
        return "{}, {}".format(self.pos_x, self.pos_y)

    def getValues(self) -> str:
        return "{}, {}".format(self.pos_x, self.pos_y)

class Start_node(Node):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.start = True
    
    def getValues(self) -> str:
        return "s"

class End_node(Node):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.end = True
    
    def getValues(self) -> str:
        return "x"

class Obstacle(Node):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.obstacle = True

    def __str__(self) -> str:
        return "☐"
    
    def getValues(self) -> str:
        return "☐"

class Path_node(Node):
    def __init__(self, pos_x, pos_y, endNode = None, g_cost = None, step_cost = None):
        super().__init__(pos_x, pos_y)
        self.g_cost = g_cost + step_cost # ist none when started 
        # distance to start node according to the path
        # can be calc by adding the prev g_cost of the node it came from + the cost to produce

        self.h_cost = self.get_h_cost(endNode)
        # distance to end node in the fastest way without obstacle
        # could be calculated with the pos of the end node and the own pos

        self.f_cost = self.g_cost + self.h_cost
        # a value to indicate the worth 
        # combines g_cost with h_cost
        self.checked = False
    
    def get_h_cost(self, endNode : Node) -> int:
        """
        calculates the distance of the node to the end node
        without the obstacles
        """

        dist_a = abs(endNode.pos_x - self.pos_x)
        dist_b = abs(endNode.pos_y - self.pos_y)
        
        if dist_a < dist_b:
            dist_a, dist_b = dist_b, dist_a

        distance = dist_b * 14 + (dist_a - dist_b) * 10
        
        return distance

    def __str__(self) -> str:
        return f"Pos: [{self.pos_x}, {self.pos_y}], g_cost = {self.g_cost}, h_cost = {self.h_cost}, f_cost = {self.f_cost}"

    def getValues(self) -> str:
        return f"Pos: [{self.pos_x}, {self.pos_y}], g_cost = {self.g_cost}, h_cost = {self.h_cost}, f_cost = {self.f_cost}"

class runtime:
    def __init__(self, run = True):
        self.run = run


def searchNode(field, searchType):
    for i in field.grid:
        for j in i:
            if searchType == "Start_node":
                if type(j) == Start_node:
                    return j
            elif searchType == "End_node":
                if type(j) == End_node:
                    return j
                
def stepCost(coordOne, coordTwo):
    if coordOne[0] == coordTwo[0] or coordOne[1] == coordOne[1]:
        return 10
    return 14

def pickNextNode(field) -> list:

    for row in field.grid:
        for i in row:
            if type(i) == Path_node and not i.checked:
                point = i
                break

    for row in field.grid:
        for i in row:
            if type(i) == Path_node and i.f_cost < point.f_cost and not i.checked:
                point = i

    return point


def calcNodes(node, field, run):
    round = getSurrounding(node, field)
    if type(field.grid[round[0][0]][round[0][1]]) == End_node:
        run.run = False
        print("we are at the end")

    endNode = searchNode(field, "End_node")
    if type(node) == Start_node:
        prev_gCost = 0 
    else:
        prev_gCost = node.g_cost
    for i in round:
        coordOne = [node.pos_x, node.pos_y]
        node = Path_node(i[0], i[1], endNode, prev_gCost, stepCost(coordOne, i))
        try:
            if node.g_cost < field.grid[i[0]][i[1]].g_cost:
                field.grid[i[0]][i[1]] = node
        except:
            field.grid[i[0]][i[1]] = node
    

def a_star(field, run):
    """
    note:
    -clean this whole code up.
    -how do i know if a node has already been checked ?
        -> checked variable in object ?
        -> save last check ? 
    -how do i know that i'm at the end ?
        -> if node is the only one 
        -> if node has already been checked ? 
    -how do i backtrack the best path ? 
        -> saving the prev node in the next ? 
            --> origin node save ? 
    
    """



    ## test
    root = tk.Tk()

    len = 500

    frame = tk.Frame(root, width=len, height=len)
    frame.pack()    

    placeBlocks(frame, field)

    
    ##

    startNode = searchNode(field, "Start_node")
    endNode = searchNode(field, "End_node")


    calcNodes(startNode, field, run)

    while run:
        time.sleep(0.5)
        currentNode = pickNextNode(field)
        calcNodes(currentNode, field, run)
        field.grid[currentNode.pos_x][currentNode.pos_y].checked = True
        placeBlocks(frame, field)
        # field.print()

    root.mainloop()

def placeBlocks(frame, field):  
    color = ""
    for row in field.grid:
        for object in row:
            if type(object) != Node:
                if type(object) == End_node:
                    color = "#0ff513"
                elif type(object) == Start_node:
                    color = "#f50f2e"
                elif type(object) == Path_node:
                    color = "#4d5beb"
                    block = tk.Frame(frame, bg=color, width=50, height=50)
                    block.place(x = (object.pos_x * 50), y = (object.pos_y * 50))
                    label = tk.Label(block, text=f"g: {object.g_cost}\nh: {object.h_cost}\nf: {object.f_cost}")
                    label.place(relx=0, rely=0, relheight=1, relwidth=1)
                    continue

                elif type(object) == Obstacle:
                    color = "#000000"

                block = tk.Frame(frame, bg=color, width=50, height=50)
                block.place(x = (object.pos_x * 50), y = (object.pos_y * 50))
    frame.update()

def getSurrounding(node, field : Grid) -> list:
    print(f"working on: {node.getValues()}")
    x = node.pos_x
    y = node.pos_y
    
    # dict of the position around the Node valid or not 
    positions_around = np.array([
        [x+1, y+1],
        [x+1, y],
        [x+1, y-1],
        [x, y+1],
        [x, y-1],
        [x-1, y+1],
        [x-1, y],
        [x-1, y-1]
    ])

    # filter to filter the valid positions 
    filter = []

    # checks if the positions are valid 
    for position in positions_around:
        try: 
            if ((position[0] < 0 or position[1] < 0) 
                or (type(field.grid[position[0]][position[1]]) == Start_node)
                or (type(field.grid[position[0]][position[1]]) == Obstacle)): 
                filter.append(False)
            elif type(field.grid[position[0]][position[1]]) == End_node:
                return [position]
            else: filter.append(True)
        
        except IndexError: filter.append(False)
    
    # returns only the valid positions
    return positions_around[filter]


if __name__ == '__main__':
    field = Grid(5)         # init grid with empty nodes
    
    start_node = Start_node(0, 0)
    end_node = End_node(4, 4)

    wall1 = Obstacle(2, 2)
    wall2 = Obstacle(2, 3)
    wall3 = Obstacle(2, 1)
    wall4 = Obstacle(2, 0)

    field.positionNode(start_node, end_node, wall1, wall2, wall3, wall4)

    field.print()

    run = runtime()

    a_star(field, run)

# Bastian Lipka