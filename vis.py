import tkinter as tk

def visualisation():
    root = tk.Tk()

    len = 500

    frame = tk.Frame(root, width=len, height=len)
    frame.pack()    

    placeBlocks(frame, field)

    root.mainloop()

def placeBlocks(frame, field):
    
    for row in field:
        for object in row:
            
    

if __name__ == '__main__':
    visualisation()