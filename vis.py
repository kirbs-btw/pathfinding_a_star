import tkinter as tk

def visualisation(field):
    root = tk.Tk()

    len = 500

    frame = tk.Frame(root, width=len, height=len)
    frame.pack()    

    placeBlocks(frame, field)

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
                elif type(object) == Obstacle:
                    color = "#000000"

                block = tk.Frame(frame, bg=color, width=50, height=50)
                block.place(x = (object.pos_x * 50), y = (object.pos_y * 50))
    frame.update()


if __name__ == '__main__':
    field = Grid(5)         # init grid with empty nodes
    
    start_node = Start_node(0, 0)
    end_node = End_node(4, 4)

    test = Node(0, 1)

    wall1 = Obstacle(2, 2)
    wall2 = Obstacle(2, 3)
    wall3 = Obstacle(2, 1)
    wall4 = Obstacle(2, 0)

    field.positionNode(start_node, end_node, wall1, wall2, wall3, wall4)

    visualisation(field)