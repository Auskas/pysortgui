#!/usr/bin/python3
#bubble_sort.py - bubble sorting implementation

import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False1


class BubbleSort:

    def __init__(self,array=None,size=450,gui=True,window=False,bars=False):
        self.name = 'Bubble sort algorithm'

        if array:
            self.array = array
        else:
            self.array = self.random_array(size) 
            self.array_size = size   

        if gui and window == False:
            self.window_init()
        else:
            self.window = window

        self.window.title(self.name)
        if bars:
            self.bars = bars
        else:
            self.create_bars()
        self.sort() 

    def __str__(self):
        return ' '.join(str(elem) for elem in self.array)  

    def random_array(self, size=10):
        return [random.randint(1,size) for i in range(size)]

    def sort(self):
        end_index = len(self.array) - 1
        while end_index > 0:
            for i in range(end_index):
                if self.array[i+1] < self.array[i]:
                    self.array[i], self.array[i+1] = self.array[i+1], self.array[i]
                    self.swap_bars(self.bars[i], self.bars[i+1])
                    self.bars[i], self.bars[i+1] = self.bars[i+1], self.bars[i]
                self.show_process(i+1)
            self.window.canvas.itemconfig(self.bars[end_index], fill='green')
            end_index -= 1
        for bar in self.bars:
            self.window.canvas.itemconfig(bar, fill='green')
            self.window.canvas.update()

    def show_process(self, current_index): 
        self.window.canvas.itemconfig(self.bars[current_index], fill='blue')
        if current_index > 0:
            self.window.canvas.itemconfig(self.bars[current_index-1], fill='white')
        self.window.canvas.update()

    def swap_bars(self, left_bar, right_bar):
        #time.sleep(0.01)
        left_bar_x0, _, left_bar_x1, _ = self.window.canvas.coords(left_bar)
        right_bar_x0, _, right_bat_x1, _ = self.window.canvas.coords(right_bar)
        self.window.canvas.move(left_bar, right_bar_x0 - left_bar_x0, 0)
        self.window.canvas.move(right_bar, left_bar_x1 - right_bat_x1, 0)
        self.window.canvas.update()

    def window_init(self):
        self.window = Tk()
        self.window.title('Bubblesort')
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
            self.bars.append(self.window.canvas.create_rectangle(x0, y0, x1, y1, fill="white"))
        self.window.canvas.update()

if __name__ == '__main__':
    array = [15,6,20,35,9,22,24,7,21,13,2,3,6,14,1,10,16,15,5,4,11,8,12]
    bubble = BubbleSort(gui=gui)
    if gui:
        try:
            bubble.window.mainloop()
        except KeyboardInterrupt:
            bubble.window.close()
