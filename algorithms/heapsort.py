#!/usr/bin/python3
#heapsort.py - heapsort implementation.

import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False

class HeapSort:

    def __init__(self,array=None,size=300,gui=True,window=False,bars=False,reverse=False):
        self.name = 'Heapsort algorithm'
        self.gui = gui

        if array:
            self.array = array
            self.array_size = len(self.array)
        else:
            self.array = self.random_array(size) 
            self.array_size = size   

        if self.gui and window == False:
            self.window_init()
        else:
            self.window = window

        if self.gui:
            self.window.title(self.name)
            if bars:
                self.bars = bars
            else:
                self.create_bars()

        self.sort() 

        if self.gui:
            for bar in self.bars:
                self.window.canvas.itemconfig(bar, fill='green')   
                self.window.canvas.update()

    def __str__(self):
        return ' '.join(str(elem) for elem in self.array)  

    def random_array(self, size=10):
        return [random.randint(1,size) for i in range(size)]

    def heapify(self, n, i):
        """ 
        This method gets: 
        n - current unsorted array size, i - current root element index.
        
        This method returns nothing.
        """
        largest = i  # Initialize largest as root
        l = 2 * i + 1     # left = 2*i + 1
        r = 2 * i + 2     # right = 2*i + 2
     
        # See if left child of root exists and it is greater than root.
        if l < n and self.array[largest] < self.array[l]:
            largest = l
     
        # See if right child of root exists and it is greater than root.
        if r < n and self.array[largest] < self.array[r]:
            largest = r
     
        # If one of the children is bigger than root, they are swapped.
        if largest != i:
            if self.gui:
                # swapping bars.
                self.window.canvas.itemconfig(self.bars[i], fill='blue')
                self.window.canvas.itemconfig(self.bars[largest], fill='blue')
                self.window.canvas.update()
                self.swap_bars(self.bars[i], self.bars[largest])
                self.bars[i], self.bars[largest] = self.bars[largest], self.bars[i]
                self.window.canvas.itemconfig(self.bars[i], fill='white')
                self.window.canvas.itemconfig(self.bars[largest], fill='white')
                self.window.canvas.update()
            
            self.array[i], self.array[largest] = self.array[largest], self.array[i]  # swap
            # Heapify the root.
            self.heapify(n, largest)
     
    
    def sort(self):
        # The main function to sort an array of given size
        # Build a maxheap.
        for i in range(self.array_size//2 - 1, -1, -1):
            self.heapify(self.array_size, i)
     
        # One by one extract elements
        for i in range(self.array_size-1, 0, -1):
            if self.gui:
                self.window.canvas.itemconfig(self.bars[0], fill='blue')
                self.window.canvas.itemconfig(self.bars[i], fill='blue')
                self.window.canvas.update()
                self.swap_bars(self.bars[0], self.bars[i])
                self.bars[i], self.bars[0] = self.bars[0], self.bars[i]
                self.window.canvas.itemconfig(self.bars[i], fill='green')
                self.window.canvas.itemconfig(self.bars[0], fill='white')
                self.window.canvas.update()
            self.array[i], self.array[0] = self.array[0], self.array[i]  # swap
            self.heapify(i, 0)

    def swap_bars(self, left_bar, right_bar):
        left_bar_x0, _, left_bar_x1, _ = self.window.canvas.coords(left_bar)
        right_bar_x0, _, right_bat_x1, _ = self.window.canvas.coords(right_bar)
        self.window.canvas.move(left_bar, right_bar_x0 - left_bar_x0, 0)
        self.window.canvas.move(right_bar, left_bar_x1 - right_bat_x1, 0)
        self.window.canvas.update()

    def create_bars(self):
        self.bars = []

        for x,y in enumerate(self.array):
            x0 = x * self.window.bar_width
            y0 = self.window.window_height - y * self.window.height_coeff
            x1 = x0 + self.window.bar_width + 1
            y1 = self.window.window_height
            self.bars.append(
                self.window.canvas.create_rectangle(
                    x0, 
                    y0, 
                    x1, 
                    y1, 
                    fill="white",
                    width=0
                )
            )
        self.window.canvas.update()

    def window_init(self):
        self.window = Tk()
        self.window.title('Quicksort')
        self.window.configure(bg='black')
        self.window.window_width = self.window.winfo_screenwidth()
        self.window.window_height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (self.window.window_width, self.window.window_height))
        self.window.canvas = Canvas(
            self.window, 
            width=self.window.window_width, 
            height=self.window.window_height, 
            bg='black'
        )
        self.window.canvas.pack()

        self.window.bar_width = self.window.window_width / self.array_size
        self.window.height_coeff = self.window.window_height / self.array_size

if __name__ == '__main__':
    gui = True
    array = [6,1,3,5,4,2]
    bubble = HeapSort(gui=gui)
    #print(bubble)
    if gui:
        try:
            bubble.window.mainloop()
        except KeyboardInterrupt:
            bubble.window.close()
