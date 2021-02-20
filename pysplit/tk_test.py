import tkinter as tk
# from tkinter import font
# from tkinter import ttk


FONT = 'Helvetica'


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(width=400, height=600)
        self.widgets = []

        self.make_menu()
        self.make_widgets()
        print(self.widgets)

        self.bind('<Button-3>', self.popup)

    def make_menu(self):
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label='hello', command=self.hello)
        menu.add_separator()
        menu.add_command(label='exit', command=self.destroy)
        self.menu = menu

    def popup(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def hello(self):
        print('hello')


    def make_widgets(self):
        label_title = LabelTitle(self, text='Title')
        label_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.widgets.append(label_title)

        split_box = SplitBox(self)
        split_box.grid(row=1, column=0, sticky=tk.NSEW)
        self.widgets.append(split_box)

        button = tk.Button(self, text='button')
        button.grid(row=2, column=0, sticky=tk.NSEW)

        row_weights = (1, 8, 1)
        for row, weight in zip(range(3), row_weights):
            self.grid_rowconfigure(row, weight=weight)
        for col in range(1):
            self.grid_columnconfigure(col, weight=1)

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


class SplitBox(tk.Listbox):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.make_widgets()

    def make_widgets(self):
        list_icon = tk.Label(self, text='hi')
        list_icon.grid(row=0, column=0, sticky='new')

        list_name = tk.Label(self, text='hi', anchor='w')
        list_name.grid(row=0, column=1, sticky='new')
        list_name.config(width=0)

        list_split = tk.Label(self, text='hi', anchor='e')
        list_split.grid(row=0, column=2, sticky='new')
        list_split.config(width=0)

        for row in range(1):
            self.grid_rowconfigure(row, weight=1)
        col_weights = [1, 6, 1]
        for col, weight in zip(range(3), col_weights):
            self.grid_columnconfigure(col, weight=weight)


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
        width = event.width // 8
        height = event.height // 2 // 2
        size = min((width, height))
        self.button_change.config(font=(FONT, size))
        self.button_exit.config(font=(FONT, size))


if __name__ == '__main__':
    app = Application()
    app.mainloop()
