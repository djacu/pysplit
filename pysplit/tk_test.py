"""Creates a stopwatch split timer for speedruns."""
import tkinter as tk


FONT = 'Helvetica'


# pylint: disable=too-many-ancestors
class Application(tk.Tk):
    """Creates the top-level application."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minsize(width=400, height=600)
        self.widgets = []

        self.make_menu()
        self.make_widgets()

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


class LabelClick(tk.Label):
    """Creates a label that can be changed by double-clicking."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.bind('<Double-Button-1>', self.update_label)

    def update_label(self, event):
        """Allows the text to be changed by double-clicking."""
        TextEditBox(self)


class TopLevelBase(tk.Toplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root
        self.attributes('-type', 'dock')
        self.x_start = None
        self.y_start = None

        self.min_geometry = (80, 40)

        x_position = self.root.winfo_rootx() + 20
        y_position = self.root.winfo_rooty() + 20
        self.geometry(f'+{x_position}+{y_position}')

        self.bind('<ButtonPress-1>', self.move_press)
        self.bind('<ButtonRelease-1>', self.move_release)
        self.bind('<B1-Motion>', self.move)
        self.bind('<B3-Motion>', self.resize)

    def move_press(self, event):
        """Stores the original position for movement."""
        self.x_start = event.x
        self.y_start = event.y

    def move_release(self, event):
        """Destroys the original position for movement."""
        self.x_start = None
        self.y_start = None

    def move(self, event):
        """Moves the window."""
        delta_x = self.winfo_pointerx() - self.x_start
        delta_y = self.winfo_pointery() - self.y_start
        self.geometry(f'+{delta_x}+{delta_y}')

    def resize(self, event):
        """Resizes the window."""
        width = self.winfo_pointerx() - self.winfo_rootx()
        height = self.winfo_pointery() - self.winfo_rooty()
        width = max(self.min_geometry[0], width)
        height = max(self.min_geometry[1], height)
        self.geometry(f'{width}x{height}')


class TextEditBox(TopLevelBase):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root
        self.default = 'Enter a new label.'

        self.geometry('400x60')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.make_widgets()

    def make_widgets(self):
        """Makes all the widgets."""
        self.make_entry()
        self.make_buttons()

    def make_entry(self):
        """Makes the entry widget."""
        entry = tk.Entry(self)
        entry.grid(row=0, column=0)
        entry.config(width=self.winfo_reqwidth())
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
        frame = tk.Frame(self)
        frame.grid(row=1, column=0, sticky=tk.NSEW)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(1):
            frame.grid_rowconfigure(row, weight=1)

        button_change = tk.Button(frame, text='Change', command=self.get_text)
        button_change.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_change = button_change

        button_exit = tk.Button(frame, text='Exit', command=self.destroy)
        button_exit.grid(row=0, column=1, sticky=tk.NSEW)
        self.button_exit = button_exit

    def get_text(self):
        """Gets the text from the entry box and modifies the parent text."""
        entry_text = self.entry.get()
        if entry_text and not entry_text == self.default:
            self.root['text'] = entry_text
            self.destroy()


if __name__ == '__main__':
    APP = Application()
    APP.mainloop()
