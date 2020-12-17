#!/usr/bin/python3
#insertion.py - insertion sorting implementation

import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False

class InsertionSort:

    def __init__(self,array=None,size=300,gui=True,window=False,bars=False,reverse=False):
        self.name = 'Insertion sort algorithm'
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

    def sort(self):
        current_index = 1
        while current_index < len(self.array):
            temp_index = current_index
            while temp_index > 0 and self.array[temp_index] < self.array[temp_index - 1]:
                self.swap_bars(self.bars[temp_index - 1], self.bars[temp_index])
                self.array[temp_index], self.array[temp_index - 1] = self.array[temp_index - 1], self.array[temp_index]
                self.bars[temp_index], self.bars[temp_index - 1] = self.bars[temp_index - 1], self.bars[temp_index]
                temp_index -= 1
            self.window.canvas.itemconfig(self.bars[temp_index], fill='white')
            self.window.canvas.update()
            current_index += 1

    def swap_bars(self, left_bar, right_bar):
        left_bar_x0, _, left_bar_x1, _ = self.window.canvas.coords(left_bar)
        right_bar_x0, _, right_bat_x1, _ = self.window.canvas.coords(right_bar)
        self.window.canvas.move(left_bar, right_bar_x0 - left_bar_x0, 0)
        self.window.canvas.move(right_bar, left_bar_x1 - right_bat_x1, 0)
        self.window.canvas.itemconfig(right_bar, fill='blue')
        self.window.canvas.itemconfig(left_bar, fill='white')
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
    gui=True
    #array = [15,6,20,35,9,22,24,7,21,13,2,3,6,14,1,10,16,15,5,4,11,8,12]
    insertion = InsertionSort(gui=gui)
    if gui:
        try:
            insertion.window.mainloop()
        except KeyboardInterrupt:
            insertion.window.close()