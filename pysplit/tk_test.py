"""Creates a stopwatch split timer for speedruns."""
import tkinter as tk


FONT = 'Helvetica'


class Application(tk.Tk):
    """Creates the top-level application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(width=400, height=600)
        self.widgets = []

        self.make_menu()
        self.make_widgets()
        print(self.widgets)

        self.bind('<Button-3>', self.popup)

    def make_menu(self):
        """Construct the top-levle right-click context menu."""
        menu = tk.Menu(self, tearoff=False)
        menu.add_command(label='hello', command=self.hello)
        menu.add_separator()
        menu.add_command(label='exit', command=self.destroy)
        self.menu = menu

    def popup(self, event):
        """Binding for the top-level right-click context menu."""
        self.menu.tk_popup(event.x_root, event.y_root)

    def hello(self):
        print('hello')

    def make_widgets(self):
        """Makes all the widgets."""
        self.make_title()
        self.make_splitbox()
        self.make_button()
        self.config_grid()

    def make_title(self):
        """Makes the title."""
        label_title = LabelClick(self, text='Title')
        label_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.widgets.append((label_title, 1))

    def make_splitbox(self):
        """Makes the main splits area."""
        split_box = SplitBox(self)
        split_box.grid(row=1, column=0, sticky=tk.NSEW)
        self.widgets.append((split_box, 8))

    def make_button(self):
        """Dummy button for now."""
        button = tk.Button(self, text='button')
        button.grid(row=2, column=0, sticky=tk.NSEW)
        self.widgets.append((button, 1))

    def config_grid(self):
        """Configures the top-level widgets grid."""
        row_weights = tuple(zip(*self.widgets))[1]
        for row, weight in zip(range(3), row_weights):
            self.grid_rowconfigure(row, weight=weight)
        for col in range(1):
            self.grid_columnconfigure(col, weight=1)

class LabelClick(tk.Label):
    """Creates a label that can be changed by double-clicking."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.bind('<Double-Button-1>', self.update_label)

    def update_label(self, event):
        """Allows the text to be changed by double-clicking."""
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)
        top.attributes('-topmost', 1)
        x_position = self.root.winfo_rootx() + 20
        y_position = self.root.winfo_rooty() + 20
        top.geometry(f'+{x_position}+{y_position}')
        box = TextEditBox(top, self)
        box.grid()


class SplitBox(tk.Listbox):
    """Creates a single split row."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.make_widgets()

    def make_widgets(self):
        """Makes all the widgets."""
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
    """Makes a popup window for editing text."""
    def __init__(self, top, root, *args, **kwargs):
        super().__init__(top, *args, **kwargs)
        self.top = top
        self.root = root
        self.default = 'Enter a new label.'

        self.top.geometry('400x60')
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=1)

        self.top.bind('<Configure>', self.resize_top)

        self.make_widgets()

    def make_widgets(self):
        """Makes all the widgets."""
        self.make_entry()
        self.make_buttons()

    def make_entry(self):
        """Makes the entry widget."""
        entry = tk.Entry(self.top)
        entry.grid(row=0, column=0)
        entry.insert(0, self.default)
        entry.config(fg='grey')
        entry.bind('<FocusIn>', self.focus_in)
        entry.bind('<FocusOut>', self.focus_out)
        self.entry = entry

    def focus_in(self, event):
        """Empties the entry if no user input."""
        if self.entry.get() == self.default:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, '')
            self.entry.config(fg='black')

    def focus_out(self, event):
        """Inserts an edit message if no user input."""
        if self.entry.get() == '':
            self.entry.insert(0, self.default)
            self.entry.config(fg='grey')

    def make_buttons(self):
        """Makes the button widgets."""
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
        """Gets the text from the entry box and modifies the parent text."""
        entry_text = self.entry.get()
        if entry_text and not entry_text == self.default:
            self.root['text'] = entry_text
            self.top.destroy()

    def resize_top(self, event):
        """Resizes all widgets with changing window size."""
        self.resize_entry(event)
        self.resize_button_text(event)

    def resize_entry(self, event):
        """Resizes the entry with changing window size."""
        width = event.width
        self.entry.config(width=width)
        # this causes the entry box to flicker sometimes when resizing
        # height = int((event.height // 2) / 4) * 4
        # self.entry.config(font=(FONT, height))

    def resize_button_text(self, event):
        """Resizes the button font size with changing window size."""
        width = event.width // 8
        height = event.height // 2 // 2
        size = min((width, height))
        self.button_change.config(font=(FONT, size))
        self.button_exit.config(font=(FONT, size))


if __name__ == '__main__':
    APP = Application()
    APP.mainloop()
