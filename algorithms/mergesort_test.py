#!/usr/bin/python3
# mergesort.py - an implementation of the Merge sorting algorithm
# Took me a whole day to figure out how to implement visualization!!!

import copy
import random
import time
try:
    from tkinter import *
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False

class MergeSort:
    """The class represents the Merge sorting algorithm."""
    def __init__(self,array=None,size=500,gui=True,window=False,bars=False,reverse=False):
        self.name = 'Mergesort algorithm'
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
        #indices = [i for i in range(self.array_size)]
        self.sort(self.array,real_index=0) 

        if self.gui:
            for bar in self.bars:
                self.window.canvas.itemconfig(bar, fill='green')   
                self.window.canvas.update()     

    def __str__(self):
        return ' '.join(str(elem) for elem in self.array)

    def random_array(self, size=10):
        return [random.randint(1,size) for i in range(size)]

    def sort(self,array,real_index=0):
        if len(array) > 1:
            middle = len(array) // 2
            left = array[:middle]
            right = array[middle:]

            a = real_index
            b = real_index + middle

            self.sort(left,real_index=a)
            self.sort(right,real_index=b)
            i = j = k = 0
            indices = []
            while i < len(left) and j < len(right):
                if left[i] < right[j]: 
                    indices.append(real_index + i)
                    array[k] = left[i]
                    i += 1
                else:
                    indices.append(real_index + middle + j)
                    array[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                indices.append(real_index + i)
                array[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                indices.append(real_index + middle + j)
                array[k] = right[j]
                j += 1
                k += 1
            #print(f'Array: {array}, Indices: {indices}, Real index {real_index}')
            i = 0
            self.temp_bars = self.bars.copy()
            self.checked_indices = set()
            print(array,indices, real_index)
            self.update_bars(indices, real_index)

    def update_bars(self, indices, real_index, i=0, follow=False, last_index=0):
        print(i)
        if indices[i] != real_index + i and i not in self.checked_indices:
            bar1 = self.temp_bars[indices[i]]
            self.move_bar(bar1, indices[i], real_index + i)

            self.bars[real_index + i] = self.temp_bars[indices[i]]
            self.checked_indices.add(i)

            if follow == False:
                follow = True
                last_index = i

            i = indices.index(real_index + i)

            self.update_bars(indices,real_index,i,follow=follow,last_index=last_index)

        else:
            if follow:
                follow = False
                i = last_index
                last_index = None
                self.update_bars(indices,real_index,i,follow=follow,last_index=last_index)
            else:
                self.checked_indices.add(i)
                i += 1

        if len(self.checked_indices) == len(indices):
            return None
        else:
            self.update_bars(indices,real_index,i)        


    def rearrange_bars(self, indices, real_index):
        bars = self.bars.copy()
        middle = len(indices) // 2
        i = 0
        j = middle
        while i < middle and j < len(indices):
            bar1 = bars[indices[i]]
            bar2 = bars[indices[j]]
            self.move_bar(bar1, indices[i], real_index + i)
            self.move_bar(bar2, indices[j], real_index + j)

            self.bars[real_index + i] = bars[indices[i]]
            self.bars[real_index + j] = bars[indices[j]]
            i += 1
            j += 1
        while i < middle:
            bar1 = bars[indices[i]]
            self.move_bar(bar1, indices[i], real_index + i)
            self.bars[real_index + i] = bars[indices[i]]
            i += 1
        while j < len(indices):
            bar2 = bars[indices[j]]
            self.move_bar(bar1, indices[j], real_index + j)
            self.bars[real_index + j] = bars[indices[j]]  
            j += 1          

    def rearrange_bars_recursion(self, indices, real_index, i, follow=False,last_index=None):
        #print(i)
        if indices[i] != real_index + i and i not in self.checked_indices:
            bar1 = self.temp_bars[indices[i]]
            self.move_bar(bar1, indices[i], real_index + i)

            self.bars[real_index + i] = self.temp_bars[indices[i]]
            self.checked_indices.add(i)

            if follow == False:
                follow = True
                last_index = i

            i = real_index + i
            if i > len(indices) - 1:
                i = last_index

            self.rearrange_bars(indices,real_index,i,follow=follow,last_index=last_index)

        else:
            if follow:
                follow = False
                i = last_index
                last_index = None
                self.rearrange_bars(indices,real_index,i,follow=follow,last_index=last_index)
            else:
                self.checked_indices.add(i)
                i += 1

        if len(self.checked_indices) == len(indices):
            return None
        else:
            self.rearrange_bars(indices,real_index,i)

    def move_bar(self, bar, pos1, pos2):
        self.window.canvas.itemconfig(bar, fill='blue')
        self.window.canvas.update()
        cur_x = self.window.bar_width * (pos1)
        tar_x = self.window.bar_width * (pos2)
        self.window.canvas.move(bar, tar_x-cur_x, 0)
        self.window.canvas.update()
        self.window.canvas.itemconfig(bar, fill='white')
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
        #self.window.height_coeff = self.window.window_height / self.array_size
        self.window.height_coeff = self.window.window_height / self.array_size

if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    print(f'Current recursion depth is {sys.getrecursionlimit()}')
    gui = True

    #array = [4,8,7,2,11,1,3]
    #array = [3,1,2]
    array = [10,9,1,11,3,4,2,5,8,7,12,6]
    merge = MergeSort(gui=True)
    #print(merge)
    if gui:
        try:
            merge.window.mainloop()
        except KeyboardInterrupt:
            merge.window.close()
        