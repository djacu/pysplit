import tkinter as tk
from tkinter import ttk


FONT = 'Helvetica'


class Application(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.pack()

        self.data = 42

        self.widgets = []
        self.make_widgets()
        print(self.widgets)

    def make_widgets(self):
        label_title = LabelTitle(self, text='Title')
        label_title.pack()

        widget = tk.Button(self, text='Button!', command=self.message)
        widget.pack(side=tk.LEFT)
        self.widgets.append(widget)

    def message(self):
        self.data += 1
        print(f'Hello frame {self.data}')


class LabelTitle(tk.Label):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.bind('<Double-Button-1>', self.update_label)

    def update_label(self, event):
        top = tk.Toplevel(self.root)
        top.wm_title('Edit Title')
        box = TextEditBox(top, self)
        box.pack()


class TextEditBox(tk.Frame):
    def __init__(self, top, root, *args, **kwargs):
        super().__init__(top, *args, **kwargs)
        self.top = top
        self.root = root

        self.top.geometry('400x60')
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=1)

        self.top.bind('<Configure>', self.resize_top)

        self.make_widgets()

    def make_widgets(self):
        entry = tk.Entry(self.top)
        entry.grid(row=0, column=0)
        self.entry = entry

        frame = tk.Frame(self.top)
        frame.grid(row=1, column=0, sticky=tk.NSEW)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(1):
            frame.grid_rowconfigure(row, weight=1)

        button_change = tk.Button(frame, text='Change', command=self.get_text)
        button_change.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_change = button_change

        button_exit = tk.Button(frame, text='Exit', command=self.top.destroy)
        button_exit.grid(row=0, column=1, sticky=tk.NSEW)
        self.button_exit = button_exit

    def get_text(self):
        entry_text = self.entry.get()
        if entry_text:
            self.root['text'] = entry_text
            self.top.destroy()

    def resize_top(self, event):
        self.resize_entry(event)
        self.resize_button_text(event)

    def resize_entry(self, event):
        height = int((event.height // 2) / 4) * 4
        width = event.width
        # this causes the entry box to flicker sometimes when resizing
        # self.entry.config(font=(FONT, height))
        self.entry.config(width=width)

    def resize_button_text(self, event):
        width = event.width // 10
        height = event.height // 2 // 2
        size = min((width, height))
        self.button_change.config(font=(FONT, size))
        self.button_exit.config(font=(FONT, size))


if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(width=200, height=400)
    app = Application(root)
    root.mainloop()
