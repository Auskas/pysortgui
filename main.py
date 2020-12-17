#!/usr/bin/python3
# sorting_comparision.py - this module compares the performance of some well-known sorting algos.

import random
import time
import sys
import os
try:
    from tkinter import *
    from tkinter import ttk
    gui = True
except ImportError:
    print('Cannot import tkinter. Visualization is not possible.')
    gui = False
from algorithms.bubble_sort import BubbleSort
from algorithms.insertion_sort import InsertionSort
from algorithms.mergesort import MergeSort
from algorithms.quicksort import QuickSort
from algorithms.selection_sort import SelectionSort
from algorithms.heapsort import HeapSort

class Interface:

    def __init__(self, gui):
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.font_size = 18
        self.algorithms_names = [
            '',
            'Quicksort',
            'Mergesort',
            'Heapsort',
            'Bubble sort',
            'Insertion sort',
            'Selection sort',
        ]
        self.algorithms = {
            'Quicksort': QuickSort, 
            'Mergesort': MergeSort,
            'Heapsort': HeapSort, 
            'Bubble sort': BubbleSort, 
            'Insertion sort': InsertionSort,
            'Selection sort': SelectionSort
        }
        self.options = [
            'shuffled progression',
            'random numbers',
            'sorted in reverse',
            'nearly sorted'
        ]
        if gui:
            self.interface_init()
            self.interface.mainloop()

    def interface_init(self,width=720,height=576):
        self.interface = Tk()
        self.interface.title('Sorting algorithms visualizer')
        self.display_max_width = self.interface.winfo_screenwidth()
        self.display_max_height = self.interface.winfo_screenheight()
        if width:
            self.interface_width = width
        else:
            self.interface_width = self.interface.winfo_screenwidth()
        if height:
            self.interface_height = height
        else:
            self.interface_height = self.window.winfo_screenheight()
        self.interface.geometry(f'{self.interface_width}x{self.interface_height}') 
        #self.interface.configure(bg='white')  
        # Tkinter icon replacement.     
        self.interface.iconphoto(False, PhotoImage(file=f'{self.SCRIPT_DIR}{os.sep}images{os.sep}sorting.png'))

        # Interface frame inside main window with some paddings.
        self.interface_frame = Frame(self.interface)
        self.interface_frame.grid(padx=20, pady=20)

        # The number of elements frame.
        self.array_size_frame = Frame(self.interface_frame, bd=1)
        self.array_size_frame.grid(column=0,row=0,sticky='nw')

        # Legend for the number of elements.
        self.array_size_legend = Label(
            self.array_size_frame,
            text='Array size: ',
            font=('Verdana', self.font_size, 'bold')
            )
        self.array_size_legend.grid(column=0,row=0,sticky='nw')

        # Input field for the number of elements.
        self.array_size_integer = IntVar()
        self.array_size_entry = Entry(
            self.array_size_frame, 
            textvariable=self.array_size_integer,
            width=4,
            font=('Verdana', self.font_size, 'bold'),
            justify='right'
        )
        self.array_size_entry.grid(column=1,row=0,sticky='nw')
        # Sets the default value of the size of the array.
        self.array_size_integer.set(self.display_max_width // 3)

        self.array_size_integer.trace("w", self.check_number_of_elements)

        self.array_options_frame = Frame(self.interface_frame, bd=0)
        self.array_options_frame.grid(column=0, row=1, pady=20,sticky='nw')

        self.array_options_legend = Label(
            self.array_options_frame,
            bd=0,
            text='Unsorted array options:  ',
            font=('Verdana', self.font_size-4, 'bold')
            )
        self.array_options_legend.grid(column=0, row=0,sticky='nw')

        self.array_options_var = StringVar()
        self.array_options = ttk.Combobox(
            self.array_options_frame, 
            textvariable=self.array_options_var,
            values=self.options
        )
        self.array_options.grid(column=1,row=0,sticky='nw')
        self.array_options_var.set(self.options[0])
        self.array_options_var.trace("w", self.nearly_sorted_options)

        self.nearly_sorted_options_frame = Frame(self.array_options_frame, bd=0,padx=20)
        #self.nearly_sorted_options_frame.grid(column=2,row=0,sticky='nw')

        self.nearly_sorted_options_legend = Label(
            self.nearly_sorted_options_frame,
            bd=0,
            text='k= ',
            font=('Verdana', self.font_size-4, 'bold')
        )
        self.nearly_sorted_options_legend.pack(side=LEFT)

        self.nearly_sorted_options_var = IntVar()
        self.nearly_sorted_options_entry = Entry(
            self.nearly_sorted_options_frame, 
            textvariable=self.nearly_sorted_options_var,
            width=4,
            font=('Verdana', self.font_size - 8, 'bold'),
            justify='right'
        )   
        self.nearly_sorted_options_entry.pack(side=LEFT)    
        self.nearly_sorted_options_var.set(self.array_size_integer.get() // 10)
        self.nearly_sorted_options_var.trace("w", self.check_k_value)
        #self.nearly_sorted_options_frame.grid_forget()
        # Checkbox frame to either set the random elements or make them unique.
        #self.random_elements_frame = Frame(self.interface_frame, bd=0)
        #self.random_elements_frame.grid(column=0, row=1, pady=10,sticky='nw')

        #self.random_array = IntVar()
        #self.random_elements_checkbox = Checkbutton(
            #self.random_elements_frame,
            #text='random elements',
            #font=('Verdana', self.font_size-4, 'bold'),
            #variable=self.random_array, 
            #onvalue=1, 
            #offvalue=0    
        #)
        #self.random_elements_checkbox.grid(column=0,row=0,sticky='ne')

        # Checkbox frame to set the fullscreen mode.
        self.fullscreen_mode_frame = Frame(self.interface_frame, bd=0)
        self.fullscreen_mode_frame.grid(column=0, row=2, pady=10,sticky='nw')

        self.fullscreen_mode_var = IntVar()
        self.fullscreen_mode_checkbox = Checkbutton(
            self.fullscreen_mode_frame,
            text='fullscreen mode',
            font=('Verdana', self.font_size-4, 'bold'),
            variable=self.fullscreen_mode_var, 
            onvalue=1, 
            offvalue=0    
        )
        self.fullscreen_mode_checkbox.grid(column=0,row=0,sticky='ne')

        self.algos_legend = Label(
            self.interface_frame,
            bd=0,
            text='Algorithms execution order:',
            font=('Verdana', self.font_size-4, 'bold')
            )
        self.algos_legend.grid(column=0, row=3, pady=10,sticky='nw')

        self.algos_frame = Frame(self.interface_frame, bd=0)
        self.algos_frame.grid(column=0, row=4, sticky='nw')

        # First option block.
        self.first_frame = Frame(self.algos_frame,bd=0)
        self.first_frame.grid(column=0,row=0,sticky='nw')

        self.first = Label(
            self.first_frame,bd=0,
            text='1. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.first.pack(side=LEFT)
        self.algo1_var = StringVar()
        self.algo1 = ttk.Combobox(
            self.first_frame, 
            textvariable=self.algo1_var,
            values=self.algorithms_names
        )
        self.algo1.pack(side=LEFT)
        self.algo1_var.set(self.algorithms_names[1])

        # Second option block.
        self.second_frame = Frame(self.algos_frame,bd=0)
        self.second_frame.grid(column=0,row=1,sticky='nw')

        self.second = Label(
            self.second_frame,bd=0,
            text='2. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.second.pack(side=LEFT)
        self.algo2_var = StringVar()
        self.algo2 = ttk.Combobox(
            self.second_frame, 
            textvariable=self.algo2_var,
            values=self.algorithms_names
        )
        self.algo2.pack(side=LEFT)

        # Third option block.
        self.third_frame = Frame(self.algos_frame,bd=0)
        self.third_frame.grid(column=0,row=2,sticky='nw')

        self.third = Label(
            self.third_frame,bd=0,
            text='3. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.third.pack(side=LEFT)
        self.algo3_var = StringVar()
        self.algo3 = ttk.Combobox(
            self.third_frame, 
            textvariable=self.algo3_var,
            values=self.algorithms_names
        )
        self.algo3.pack(side=LEFT)

        # Fourth option block.
        self.fourth_frame = Frame(self.algos_frame,bd=0)
        self.fourth_frame.grid(column=0,row=3,sticky='nw')

        self.fourth = Label(
            self.fourth_frame,bd=0,
            text='4. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.fourth.pack(side=LEFT)
        self.algo4_var = StringVar()
        self.algo4 = ttk.Combobox(
            self.fourth_frame, 
            textvariable=self.algo4_var,
            values=self.algorithms_names
        )
        self.algo4.pack(side=LEFT)

        # Fifth option block.
        self.fifth_frame = Frame(self.algos_frame,bd=0)
        self.fifth_frame.grid(column=0,row=4,sticky='nw')

        self.fifth = Label(
            self.fifth_frame,bd=0,
            text='5. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.fifth.pack(side=LEFT)
        self.algo5_var = StringVar()
        self.algo5 = ttk.Combobox(
            self.fifth_frame, 
            textvariable=self.algo5_var,
            values=self.algorithms_names
        )
        self.algo5.pack(side=LEFT)

        # Sixth option block.
        self.sixth_frame = Frame(self.algos_frame,bd=0)
        self.sixth_frame.grid(column=0,row=5,sticky='nw')

        self.sixth = Label(
            self.sixth_frame,bd=0,
            text='6. ',
            font=('Verdana', self.font_size-4, 'bold')
            )         
        self.sixth.pack(side=LEFT)
        self.algo6_var = StringVar()
        self.algo6 = ttk.Combobox(
            self.sixth_frame,
            textvariable=self.algo6_var,
            values=self.algorithms_names
        )
        self.algo6.pack(side=LEFT)

        # Run button
        self.run_button = Button(
            self.interface_frame,
            text='Run simulation',
            font=('Verdana', self.font_size, 'bold'),
            command=self.run_sorting_algorithms
        )
        self.run_button.grid(column=0, row=8, pady=50, sticky='nw')

    def check_number_of_elements(self,*args):
        # An exception catcher is added to make sure that the input field
        # is not an empty string.
        try:
            entered_number_of_elements = self.array_size_integer.get()
        except Exception as exc:
            return
        # The width of a single bar cannot be less than 1 pixel.
        if entered_number_of_elements > self.display_max_width:
            self.array_size_integer.set(self.display_max_width)

    def nearly_sorted_options(self,*args):
        if self.array_options_var.get() == self.options[3]:
            self.nearly_sorted_options_frame.grid(column=2,row=0,sticky='nw')
        else:
            self.nearly_sorted_options_frame.grid_forget()

    def check_k_value(self,*args):
        # An exception catcher is added to make sure that the input field
        # is a valid number
        try:
            k = self.nearly_sorted_options_var.get()
            k = int(k)
        except Exception as exc:
            return
        if k < 0:
            self.nearly_sorted_options_var.set(1)
        if k > self.display_max_width:
            self.nearly_sorted_options_var.set(self.display_max_width)
        
    def window_init(self,width=None,height=None,fullscreen=False):
        self.window = Toplevel()
        self.window.title('Running algorithms...')
        self.window.configure(bg='black')
        if width:
            self.window.window_width = width
        else:
            self.window.window_width = self.display_max_width
        if height:
            self.window.window_height = height
        else:
            self.window.window_height = self.display_max_height

        self.window.bind("<Escape>", self.window_destroy)

        if fullscreen:
            self.window.geometry(f'{self.window.window_width}x{self.window.window_height}')
            self.window.attributes('-fullscreen',True)
        else:
            self.window.geometry(f'{self.window.window_width}x{self.window.window_height}')
        self.window.canvas = Canvas(
            self.window, 
            width=self.window.window_width, 
            height=self.window.window_height, 
            bg='black'
        )
        self.window.canvas.pack()
        self.window.bar_width = self.window.window_width / self.array_size
        print(f'Bars width: {self.window.bar_width}')
        self.window.height_coeff = self.display_max_height / self.array_size
        #self.window.lift()
        self.window.focus_force()

    def create_bars(self,array):
        self.bars = []

        for x,y in enumerate(array):
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

    def random_array_generator(self, size=10, min_=1, max_=50):
        self.array = [random.randint(min_,size) for i in range(size)]

    def array_generator(self, size=10, min=1):
        self.array = [int(i) for i in range(size)]
        random.shuffle(self.array)

    def reverse_array_generator(self, min_=1, size=10):
        self.array = [int(i) for i in range(size,-1,-1)]

    def nearly_sorted_generator(self, min_=1, size=10, k=10):
        # Get a sorted arithmetic progression array.
        self.array = [int(i) for i in range(size)]
        # Permutate some of its elements based on k.
        for i in range(size):
            new_pos_i = i + random.randint(-k, k)
            if new_pos_i < 0 or new_pos_i > size - 1:
                continue
            self.array[i], self.array[new_pos_i] = self.array[new_pos_i], self.array[i]

    def run_sorting_algorithms(self):
        # Make sure that the entered array size is am integer.
        try:
            self.array_size = self.array_size_integer.get()
            self.array_size = int(self.array_size)
        except Exception:
            self.array_size = self.display_max_width // 3

        # Get options of the unsorted array.
        option = self.array_options_var.get()
        # A simple case - the array is a shuffled arithmetic progression.
        if option == self.options[0]:
            self.array_generator(size=self.array_size)
        # The array is generated using random integers.
        elif option == self.options[1]:
            self.random_array_generator(
                size=self.array_size,
                max_=self.display_max_height
            )
        # The array is sorted in reverse.
        elif option == self.options[2]:
            self.reverse_array_generator(size=self.array_size)
        # The array is K-sorted.
        elif option == self.options[3]:
            try:
                k = self.nearly_sorted_options_var.get()
                int(k)
            except Exception:
                k = 10
            self.nearly_sorted_generator(size=self.array_size, k=k)

        # Initialization of Toplevel window...
        fullscreen = self.fullscreen_mode_var.get()
        self.window_init(fullscreen=fullscreen)

        chosen_algos = (
            self.algo1_var.get(),
            self.algo2_var.get(),
            self.algo3_var.get(),
            self.algo4_var.get(),
            self.algo5_var.get(),
            self.algo6_var.get()
        )
        
        for algo in chosen_algos:
            initial_array = self.array.copy()
            self.window.canvas.delete('all')
            if algo in self.algorithms.keys():
                self.create_bars(initial_array)
                self.algorithms[algo](
                    array=initial_array, 
                    window=self.window,
                    bars=self.bars
                )
                # Time in seconds between the algos.
                time.sleep(2)
        self.window.destroy()

    def window_destroy(self, event):
        self.window.destroy()


if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    print(f'Current recursion depth is {sys.getrecursionlimit()}')
    interface = Interface(gui)
    #ARRAY_SIZE = 100000
    #MIN_INT = 1
    #MAX_INT = 500000
    
    #array = random_array(ARRAY_SIZE,MIN_INT,MAX_INT)
    #print(f'The array size is {ARRAY_SIZE} random elements from {MIN_INT} to {MAX_INT}')
    #run_sorting_algorithms(array)
    