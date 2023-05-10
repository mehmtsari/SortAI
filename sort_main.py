import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np

import time


class SortAI:
    def __init__(self):
        self.main = tk.Tk()
        self.main.title("Sort AI")
        self.main.geometry("1280x720")
        self.main.minsize(1280,720)
        self.main.configure(background="#000000")
        
        # self.main üzerinde soldaki frame 1x sağdaki frame 4x katı büyüklükte olmak üzere iki adet frame oluşturuldu.
        
        self.left_frame = tk.Frame(self.main, width=200, height=720, bg="#000000")
        self.left_frame.grid(row=0, column=0)
        
        self.right_frame = tk.Frame(self.main, width=1080, height=720, bg="#ffffff")
        self.right_frame.grid(row=0, column=1)
        
        # Left fram üzerindeki adımlar
        data_size_label = tk.Label(self.left_frame, text="Data Size", font=("Arial"), bg="#000000", fg="#ffffff")
        data_size_label.grid(row=0, column=0, padx=10, pady=10)
        self.data_size = tk.Entry(self.left_frame, font=("Arial", 20) ,width=15)
        self.data_size.grid(row=1, column=0, padx=10, pady=10)
        
        
        data_min_label = tk.Label(self.left_frame, text="Minimum İnt (Default: 0)", font=("Arial"), bg="#000000", fg="#ffffff")
        data_min_label.grid(row=2, column=0)
        self.data_min = tk.Entry(self.left_frame,  font=("Arial", 20) ,width=10)
        self.data_min.grid(row=3, column=0)
        
        data_max_label = tk.Label(self.left_frame, text="Maximum İnt (Default: 100)", font=("Arial"), bg="#000000", fg="#ffffff")
        data_max_label.grid(row=4, column=0, padx=10, pady=10)
        self.data_max = tk.Entry(self.left_frame,  font=("Arial", 20) ,width=10)
        self.data_max.grid(row=5, column=0, padx=10, pady=10)
        
         # listedeki verilerden oluşan radiobuttonlar oluşturuldu. Altında bulunan butona tıklandığında listbox da seçili olan veri print edilecek.
        
        radio_button_frame = tk.Frame(self.left_frame,bg="#000000" )
        radio_button_frame.grid(row=6, column=0, padx=10, pady=10 )
        
        self.filters = ['Bubble Sort','Insertion Sort','Selection Sort','Quick Sort']
        self.selected_filter = tk.StringVar(value=self.filters[1])
        
        self.radio_buttons = []
        for filter in self.filters:
            rb = tk.Radiobutton(radio_button_frame, text=filter, variable=self.selected_filter, value=filter, bg="#000000", fg="#ffffff",font=("Arial", 14), selectcolor="red",activeforeground='red', bd=0, indicatoron=0)
            self.radio_buttons.append(rb)
        
        for rb in self.radio_buttons:
            rb.pack(anchor=tk.E)
            
        start_button = tk.Button(self.left_frame, text="Start", font=("Arial", 20), bg="#000000", fg="#ffffff", command=self.start)
        start_button.grid(row=7, column=0, padx=10, pady=10)

        self.main.mainloop()
        
    def bubble_sort(self,data):
        self.stop_code = False
        n = len(data)
        self.counter = []
        for i in range(n):
            for i,j in enumerate(range(n-i-1)):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    self.changed_items = True
                    self.counter = j + 1
                    yield data
                    continue
                self.changed_items = False
                self.counter = j + 1
                yield data
            self.finished_rects.append(self.counter)
            yield data
        self.finished_rects.append(0)
        self.stop_code = True
        yield data
        
    def insertion_sort(self,data):
        self.checked_items = [0,0]
        self.stop_code = False
        n = len(data)
        for i in range(1, n):
            key = data[i]
            j = i - 1
            while j >= 0 and key <= data[j]:
                data[j + 1] = data[j]
                self.checked_items = [i, j]
                j -= 1
                yield data
            data[j + 1] = key
            yield data
        self.stop_code = True
        yield data
    
    def selection_sort(self,data):
        self.finished_rects = []
        self.stop_code = False
        for i in range(len(data)):
            for j in range(i+1, len(data)):
                self.checked_items = [j,i,None]
                if data[j] < data[i]:
                    data[i], data[j] = data[j], data[i]
                    self.checked_items = [i,j,j]
                else:
                    self.checked_items = [i,j,None]
                yield data
            self.finished_rects.append(i)
        self.stop_code = True
        yield data
    
    def quick_sort(self,data):
        stack = [(0, len(data)-1)]
        result = []
        step = 1
        self.finished_rects = []
        while stack:
            print(f"Adım {step}: {data}")
            step += 1
            
            left, right = stack.pop()
            print(f"\tleft: {left}, right: {right}")
            for i in range(right+1,len(data)):
                if i not in self.finished_rects:
                    self.finished_rects.append(i)
            
            if right - left < 1:
                continue
            
            self.pivot = data[right]
            self.pivot_index = right
            i = left
            for j in range(left, right):
                if data[j] < self.pivot:
                    print(f'\t{data[j]} < {self.pivot} olduğu için yer değiştirmiyoruz: {data}')
                    data[i], data[j] = data[j], data[i]
                    self.checked_items = [i, j,True]
                    yield data
                    i += 1
            data[i], data[right] = data[right], data[i]
            print(f"\tYer değiştiriyor {data[i]} with {data[right]}: {data}")
            self.checked_items = [j,i,True]
            yield data
                        
            stack.append((left, i-1))
            stack.append((i+1, right))
        print(f"Final sorted dataay: {data}")
        self.finished_rects.append(0)
        yield data
        return data
            
    def create_widgets(self):
        # rastgele sayılardan oluşan bir dizi oluşturalım
        self.data = np.random.randint(int(self.data_min.get()),int(self.data_max.get()),size=int(self.data_size.get()))
        self.finished_rects = []
        
        # çizim için bir figür oluşturalım ve büyüklüğü right_frame e göre ayarlayalım
        self.fig = Figure(figsize=(10.8, 7.2), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        
        self.ax.set_ylabel("Value")
        self.bar_rects = self.ax.bar(range(len(self.data)), self.data, align="edge")
        # sola yaslı title label text ekleyelim
        self.title_label = self.ax.text(0.02, 0.95, "",bbox={"facecolor":"white", "alpha":0.5, "pad":5}, transform=self.ax.transAxes)
        self.title_label.set_text(self.selected_filter_data)
        self.bar_labels = []
        for rect in self.bar_rects:
            height = rect.get_height()
            label = self.ax.text(rect.get_x() + rect.get_width() / 2, height, "", ha="center", va="bottom")
            self.bar_labels.append(label)

        

        # animasyon işlemi için kullanacağımız fonksiyonu tanımlayalım
        def update_fig_bubble(data):
            for c, (rect, val) in enumerate(zip(self.bar_rects, data)):
                
                if self.counter == c:
                    second_rect = self.counter -1
                    finished_rect = self.counter
                    if self.changed_items:
                        self.bar_rects[self.counter].set_color("red")
                        self.bar_rects[second_rect].set_color("red")
                    else:
                        self.bar_rects[self.counter].set_color("orange")
                        self.bar_rects[second_rect].set_color("blue")
                    
                else:
                    rect.set_color("#666666")
                
                rect.set_height(val)
                self.bar_labels[c].set_text(val)
                self.bar_labels[c].set_position((rect.get_x() + rect.get_width() / 2, rect.get_height()))
                
                for frect in self.finished_rects:
                        self.bar_rects[frect].set_color("green")
                        if frect == 0:
                            self.animation.event_source.stop()
        
        def update_fig_insertion(data):
            for c, (rect, val) in enumerate(zip(self.bar_rects, data)):
                if c == self.checked_items[0]:
                    rect.set_color("blue")
                elif c == self.checked_items[1]:
                    rect.set_color("orange")
                else:
                    rect.set_color("#666666")
                
                rect.set_height(val)
                self.bar_labels[c].set_text(val)
                self.bar_labels[c].set_position((rect.get_x() + rect.get_width() / 2, rect.get_height()))
                
                if self.stop_code == True:
                    for rect in self.bar_rects:
                        rect.set_color("green")
                    self.animation.event_source.stop()
        
        def update_fig_selection(data):
            for c, (rect, val) in enumerate(zip(self.bar_rects, data)):
                
                
                if c == self.checked_items[0]:
                    rect.set_color('blue')
                elif c == self.checked_items[1] and self.checked_items[2] is None:
                    rect.set_color('orange')
                elif c == self.checked_items[2] and self.checked_items[2] is not None:
                    rect.set_color('red')
                else:
                    rect.set_color('#666666')
                

                
                
                rect.set_height(val)
                self.bar_labels[c].set_text(val)
                self.bar_labels[c].set_position((rect.get_x() + rect.get_width() / 2, rect.get_height()))
                
                for frect in self.finished_rects:
                    self.bar_rects[frect].set_color("green")
                
                if self.stop_code == True:

                    self.animation.event_source.stop()
        
        def update_fig_quick(data):
            for c, (rect, val) in enumerate(zip(self.bar_rects, data)):
                
                if c == self.checked_items[0]:
                    if self.checked_items[2]:
                        rect.set_color('red')
                    else:
                        rect.set_color('blue')
                elif c == self.checked_items[1]:
                    rect.set_color('orange')
                else:
                    rect.set_color('#666666')
                
                if c == self.pivot_index:
                    rect.set_color('blue')
                
                for frect in self.finished_rects:
                    self.bar_rects[frect].set_color("green")
                
                
                    
                rect.set_height(val)
                self.bar_labels[c].set_text(val)
                self.bar_labels[c].set_position((rect.get_x() + rect.get_width() / 2, rect.get_height()))
                
        

                
            
                       
        # FuncAnimation ile animasyonu oluşturalım
        # canvas oluşturalım ve figürü ekleyelim
        if self.selected_filter_data == "Bubble Sort":
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.animation = FuncAnimation(self.fig, func=update_fig_bubble, frames=self.bubble_sort(self.data.copy()), repeat=True)
        elif self.selected_filter_data == "Insertion Sort":
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.animation = FuncAnimation(self.fig, func=update_fig_insertion, frames=self.insertion_sort(self.data.copy()), repeat=True)
        elif self.selected_filter_data == 'Selection Sort':
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.animation = FuncAnimation(self.fig, func=update_fig_selection, frames=self.selection_sort(self.data.copy()), repeat=True)
        elif self.selected_filter_data == 'Quick Sort':
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.animation = FuncAnimation(self.fig, func=update_fig_quick, frames=self.quick_sort(self.data.copy()), repeat=True)
            
    def start(self):
        self.right_frame.destroy()
        self.right_frame = tk.Frame(self.main, width=1080, height=720, bg="#ffffff")
        self.right_frame.grid(row=0, column=1)
        self.selected_filter_data = self.selected_filter.get()
        print(self.selected_filter_data)
        
        self.create_widgets()
         
SortAI()