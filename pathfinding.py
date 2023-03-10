# algorithm name "A*"
import numpy as np 
import time
import tkinter as tk
import random as r

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
    def __str__(self) -> str:
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
    def __init__(self, pos_x, pos_y, endNode = None, g_cost = None, step_cost = None, origin = None):
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
        # calls for a check if the node
        # has already run the process
        self.origin = origin
        # saves the origin where the new node comes from
    
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

class Correct_node(Node):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

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
    if coordOne[0] == coordTwo[0] or coordOne[1] == coordTwo[1]:
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
    origin = node
    if type(field.grid[round[0][0]][round[0][1]]) == End_node:
        run.run = False
        print("we are at the end")
        return node
 
    endNode = searchNode(field, "End_node")
    if type(node) == Start_node:
        prev_gCost = 0 
    else:
        prev_gCost = node.g_cost
    for i in round:
        coordOne = [node.pos_x, node.pos_y]
        newnode = Path_node(i[0], i[1], endNode, prev_gCost, stepCost(coordOne, i), origin)
        try:
            print("Node g cost, existing node g cost")
            print(newnode.g_cost)
            print(field.grid[i[0]][i[1]].g_cost)
            if newnode.g_cost < field.grid[i[0]][i[1]].g_cost:
                field.grid[i[0]][i[1]] = newnode
                print("change made!")
            print()
        except:
            field.grid[i[0]][i[1]] = newnode
    

def a_star(field, run, blocksize):
    """
    note:
    -clean this whole code up.
    -how do i backtrack the best path ? 
        -> saving the prev node in the next ? 
            --> origin node save ? 
    
    """



    ## test
    root = tk.Tk()

    len = 700

    frame = tk.Frame(root, width=len, height=len)
    frame.pack()    

    placeBlocks(frame, field, blocksize)

    
    ##

    startNode = searchNode(field, "Start_node")
    endNode = searchNode(field, "End_node")


    calcNodes(startNode, field, run)

    while run.run:
        # input("ok")
        # time.sleep(0.1)
        currentNode = pickNextNode(field)
        nextNode = calcNodes(currentNode, field, run)
        
        if nextNode != None:
            backtrack(field, currentNode)
        else:
            field.grid[currentNode.pos_x][currentNode.pos_y].checked = True
        
        
        placeBlocks(frame, field, blocksize)

    root.mainloop()

def backtrack(field, node):
    while type(node) != Start_node:
        field.grid[node.pos_x][node.pos_y] = Correct_node(node.pos_x, node.pos_y)
        node = node.origin
        


def placeBlocks(frame, field, blockSize):  
    for widget in frame.winfo_children():
        widget.destroy()

    color = ""
    for row in field.grid:
        for object in row:
            if type(object) != Node:
                if type(object) == End_node:
                    color = "#0ff513"
                elif type(object) == Start_node:
                    color = "#f50f2e"
                elif type(object) == Path_node:
                    color = "#654321"
                    """
                    block = tk.Frame(frame, bg=color, width=blockSize, height=blockSize)
                    block.place(x = (object.pos_x * blockSize), y = (object.pos_y * blockSize))
                    label = tk.Label(block, text=f"g: {object.g_cost}\nh: {object.h_cost}\nf: {object.f_cost}\n o: {object.origin.pos_x}, {object.origin.pos_y}")
                    label.place(relx=0, rely=0, relheight=1, relwidth=1)
                    continue
                    """
                elif type(object) == Correct_node:
                    color = "#fff111"
                elif type(object) == Obstacle:
                    color = "#000000"

                block = tk.Frame(frame, bg=color, width=blockSize, height=blockSize)
                block.place(x = (object.pos_x * blockSize), y = (object.pos_y * blockSize))
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

def placeRandomObstacle(field, count, startNode, endNode):
    for _ in range(count):
        x = r.randint(0, (len(field.grid) - 1))
        y = r.randint(0, (len(field.grid) - 1))
        if (x == startNode.pos_x and y == startNode.pos_y) or (x == endNode.pos_x and y == endNode.pos_y):
            continue
        field.grid[x][y] = Obstacle(x, y)

if __name__ == '__main__':
    field = Grid(30)         # init grid with empty nodes
    size = 20

    start_node = Start_node(0, 0)
    end_node = End_node(25, 25)

    placeRandomObstacle(field, 299, start_node, end_node)

    field.positionNode(start_node, end_node)

    """
    start_node = Start_node(0, 0)
    end_node = End_node(45, 40)

    wall1 = Obstacle(2, 2)
    wall2 = Obstacle(2, 3)
    wall3 = Obstacle(2, 1)
    wall4 = Obstacle(2, 0)
    wall5 = Obstacle(3, 3)

    field.positionNode(start_node, end_node, wall1, wall2, wall3, wall4, wall5)
    """

    """
    start_node = Start_node(0, 0)
    end_node = End_node(4, 4)

    wall1 = Obstacle(0, 1)
    wall2 = Obstacle(1, 1)
    wall3 = Obstacle(2, 1)
    wall4 = Obstacle(3, 1)
    wall5 = Obstacle(4, 3)
    wall6 = Obstacle(1, 3)
    wall7 = Obstacle(2, 3)
    wall8 = Obstacle(3, 3)

    field.positionNode(start_node, end_node, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8)
    """

    field.print()

    run = runtime()

    a_star(field, run, size)

# Bastian Lipka

# problems
# slow af my code needs so much opt
# when old blocks are checked again they don't get changed
# --> the checkt solution is not proper because an old better node does not get checkt again
# --> existing nodes dont get changed if better option exists