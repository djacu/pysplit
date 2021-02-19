import tkinter as tk
from tkinter import ttk


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
        box.grid()


class TextEditBox(tk.Frame):
    def __init__(self, root, root2, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.root2 = root2
        self.make_widgets()

    def make_widgets(self):
        entry = tk.Entry(self.root, width=40)
        entry.grid(row=0, column=0)
        self.entry = entry

        frame = tk.Frame(self.root, width=40)
        frame.grid(row=1, column=0, sticky=tk.NSEW)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        button_change = tk.Button(frame, text='Change', command=self.get_text)
        button_change.grid(row=0, column=0, sticky=tk.NSEW)
        button_exit = tk.Button(frame, text='Exit', command=self.root.destroy)
        button_exit.grid(row=0, column=1, sticky=tk.NSEW)

    def get_text(self):
        self.root2['text'] = self.entry.get()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(width=200, height=400)
    app = Application(root)
    root.mainloop()
