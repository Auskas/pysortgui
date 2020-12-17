#!/usr/bin/python3
# selection.py - selection algorithm for sorting lists.

import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False

class SelectionSort:

    def __init__(self,array=None,size=300,gui=True,window=False,bars=False,reverse=False):
        self.name = 'Selection sort algorithm'
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

    def sort(self,reverse=False):
        for i in range(len(self.array)):
            smallest_value = self.array[i]
            smallest_value_index = i
            for j in range(i+1, len(self.array)):
                if self.array[j] < smallest_value:
                    smallest_value_index = j
                    smallest_value = self.array[j]
                if self.gui:
                    self.show_process(i,j)
                    
            if self.gui:
                self.swap_bars(self.bars[i], self.bars[smallest_value_index])
                self.bars[i], self.bars[smallest_value_index] = self.bars[smallest_value_index], self.bars[i]
                self.window.canvas.itemconfig(self.bars[i], fill='green')
                self.window.canvas.update()
            self.array[i], self.array[smallest_value_index] = self.array[smallest_value_index], self.array[i]

    def show_process(self, i, j):
        if j > i + 1:
            self.window.canvas.itemconfig(self.bars[j-1], fill='white')
        if j < self.array_size - 1:
            self.window.canvas.itemconfig(self.bars[j], fill='blue')
        self.window.canvas.update() 

    def swap_bars(self, left_bar, right_bar):
        left_bar_x0, _, left_bar_x1, _ = self.window.canvas.coords(left_bar)
        right_bar_x0, _, right_bat_x1, _ = self.window.canvas.coords(right_bar)
        self.window.canvas.move(left_bar, right_bar_x0 - left_bar_x0, 0)
        self.window.canvas.move(right_bar, left_bar_x1 - right_bat_x1, 0)
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

if __name__ == '__main__':
    gui = True
    selection = SelectionSort(gui=gui)
    if gui:
        try:
            selection.window.mainloop()
        except KeyboardInterrupt:
            selection.window.close()
