#!/usr/bin/python3
# quicksort.py - an implementation of the Quicksort algorithm.
#
import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False

class QuickSort:
    """The class represents the Quicksort algorithm."""
    def __init__(self,array=None,size=1366,gui=True,window=False,bars=False,reverse=False):
        self.name = 'Quicksort algorithm'
        self.gui = gui

        if array:
            self.array = array
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

        self.sort(0,len(self.array)-1,reverse) 

        if self.gui:
            for bar in self.bars:
                self.window.canvas.itemconfig(bar, fill='green')   
                self.window.canvas.update()

    def __str__(self):
        return ' '.join(str(elem) for elem in self.array)

    def random_array(self, size=10):
        return [random.randint(1,size) for i in range(size)]

    def partition(self, begin, end, reverse=False):
        #pivot = (begin + end) // 2
        pivot = begin
        for i in range(pivot+1, end+1):
            if self.array[i] <= self.array[begin]:
                pivot += 1
                self.array[i], self.array[pivot] = self.array[pivot], self.array[i]
                if self.gui:
                    self.window.canvas.itemconfig(self.bars[pivot], fill='blue')
                    self.window.canvas.itemconfig(self.bars[i], fill='blue')
                    self.window.canvas.update()
                    self.swap_bars(self.bars[pivot], self.bars[i])
                    self.bars[i], self.bars[pivot] = self.bars[pivot], self.bars[i]
                    self.window.canvas.itemconfig(self.bars[pivot], fill='white')
                    self.window.canvas.itemconfig(self.bars[i], fill='white')
                    self.window.canvas.update()
        if self.gui:
            self.window.canvas.itemconfig(self.bars[pivot], fill='blue')
            self.window.canvas.itemconfig(self.bars[begin], fill='blue')
            self.window.canvas.update()
            self.swap_bars(self.bars[begin], self.bars[pivot])
            self.bars[begin], self.bars[pivot] = self.bars[pivot], self.bars[begin]
            self.window.canvas.itemconfig(self.bars[pivot], fill='white')
            self.window.canvas.itemconfig(self.bars[begin], fill='white')
            self.window.canvas.update()
        self.array[pivot], self.array[begin] = self.array[begin], self.array[pivot]
        return pivot

    def sort(self,begin,end,reverse=False):
        if begin >= end:
            return
        pivot = self.partition(begin, end, reverse)
        self.sort(begin, pivot-1)
        self.sort(pivot+1, end)

    def swap_bars(self, left_bar, right_bar):
        left_bar_x0, _, left_bar_x1, _ = self.window.canvas.coords(left_bar)
        right_bar_x0, _, right_bar_x1, _ = self.window.canvas.coords(right_bar)
        self.window.canvas.move(left_bar, right_bar_x0 - left_bar_x0, 0)
        self.window.canvas.move(right_bar, left_bar_x1 - right_bar_x1, 0)
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

    def close(self, event):
        self.window.destroy()


if __name__ == '__main__':
    gui = True
    quick = QuickSort(gui=gui)
    #print(quick)
    if gui:
        try:
            quick.window.mainloop()
        except KeyboardInterrupt:
            quick.window.close()