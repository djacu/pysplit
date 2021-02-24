"""Creates a stopwatch split timer for speedruns."""
import tkinter as tk
import tkinter.ttk as ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk


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
        menu.add_command(label='editor', command=self.editor)
        menu.add_separator()
        menu.add_command(label='exit', command=self.destroy)
        self.menu = menu

    def popup(self, event):
        """Binding for the top-level right-click context menu."""
        self.menu.tk_popup(event.x_root, event.y_root)

    def editor(self):
        """Opens the editor."""
        Editor(self)

    @staticmethod
    def hello():
        """Prints 'hello'."""
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
        button = ttk.Button(self, text='button')
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
        list_icon = ttk.Label(self, text='hi')
        list_icon.grid(row=0, column=0, sticky='new')

        list_name = ttk.Label(self, text='hi', anchor='w')
        list_name.grid(row=0, column=1, sticky='new')
        list_name.config(width=0)

        list_split = ttk.Label(self, text='hi', anchor='e')
        list_split.grid(row=0, column=2, sticky='new')
        list_split.config(width=0)

        for row in range(1):
            self.grid_rowconfigure(row, weight=1)
        col_weights = [1, 6, 1]
        for col, weight in zip(range(3), col_weights):
            self.grid_columnconfigure(col, weight=weight)


class LabelClick(ttk.Label):
    """Creates a label that can be changed by double-clicking."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.bind('<Double-Button-1>', self.update_label)

    def update_label(self, event):
        """Allows the text to be changed by double-clicking."""
        # pylint: disable=unused-argument
        TextEditBox(self)


class TopLevelBase(tk.Toplevel):
    """Creates a floating dock window."""
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
        self.x_start = self.winfo_pointerx() - self.winfo_rootx()
        self.y_start = self.winfo_pointery() - self.winfo_rooty()

    def move_release(self, event):
        """Destroys the original position for movement."""
        # pylint: disable=unused-argument
        self.x_start = None
        self.y_start = None

    def move(self, event):
        """Moves the window."""
        # pylint: disable=unused-argument
        delta_x = self.winfo_pointerx() - self.x_start
        delta_y = self.winfo_pointery() - self.y_start
        self.geometry(f'+{delta_x}+{delta_y}')

    def resize(self, event):
        """Resizes the window."""
        # pylint: disable=unused-argument
        width = self.winfo_pointerx() - self.winfo_rootx()
        height = self.winfo_pointery() - self.winfo_rooty()
        width = max(self.min_geometry[0], width)
        height = max(self.min_geometry[1], height)
        self.geometry(f'{width}x{height}')


class Editor(TopLevelBase):
    """Creates an editor window for settings."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root

        self.label_pad = 16

        self.make_top_frame()
        self.make_widgets()

    def make_top_frame(self):
        """Splits the top-level into left and right columns."""
        self.grid_columnconfigure(1, weight=1)
        for row in range(1):
            self.grid_rowconfigure(row, weight=1)

    def make_widgets(self):
        """Makes all the widgets."""
        self.make_left()
        self.make_right()

    def make_left(self):
        """Makes the left widgets."""
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        # image_icon = Image.open('./images/berry.png')
        # image_icon = image_icon.resize((160, 160), Image.NEAREST)
        # icon = ImageTk.PhotoImage(image_icon)
        # label_icon = tk.Label(frame, image=icon)
        # label_icon.image = icon

        icon = tk.PhotoImage(file='./images/berry.png')
        icon = icon.zoom(10)
        label_icon = ttk.Label(frame, image=icon)
        label_icon.image = icon

        button_insert_above = ttk.Button(frame, text='Insert Above',
                                        command=self.destroy)
        button_insert_below = ttk.Button(frame, text='Insert Below',
                                        command=self.destroy)
        button_remove = ttk.Button(frame, text='Remove',
                                  command=self.destroy)
        button_move_up = ttk.Button(frame, text='Move Up',
                                   command=self.destroy)
        button_move_down = ttk.Button(frame, text='Move Down',
                                     command=self.destroy)

        widget_list = [label_icon, button_insert_above, button_insert_below,
                       button_remove, button_move_up, button_move_down]
        frame.grid_columnconfigure(0, weight=1)
        for row, widget in enumerate(widget_list):
            widget.grid(row=row, column=0, sticky=tk.NSEW)
            # frame.grid_rowconfigure(row, weight=1)

    def make_right(self):
        """Makes the right widgets."""
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        widget_name = self.make_name(right_frame)
        widget_category = self.make_category(right_frame)
        widget_time = self.make_time(right_frame)
        widget_attempts = self.make_attempts(right_frame)
        widget_tree = self.make_tree(right_frame)

        widget_list = [widget_name, widget_category, widget_time,
                       widget_attempts, widget_tree]
        right_frame.grid_columnconfigure(0, weight=1)
        for row, widget in enumerate(widget_list):
            widget.grid(row=row, column=0, sticky=tk.NSEW)
            # right_frame.grid_rowconfigure(row, weight=1)

    def make_name(self, root):
        frame_name = ttk.Frame(root)
        text = 'Game Name:'.ljust(self.label_pad)
        label_name = ttk.Label(frame_name, text=text)
        label_name.pack(side=tk.LEFT)

        name_list = ['Super Mario World', 'Super Mario Brothers', 'Zelda']

        option_name = AutocompleteCombobox(frame_name, name_list)
        option_name.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return frame_name

    def make_category(self, root):
        frame_category = ttk.Frame(root)
        text = 'Category:'.ljust(self.label_pad)
        label_category = ttk.Label(frame_category, text=text)
        label_category.pack(side=tk.LEFT)

        category_list = ['Any%', '100%', 'Low%', 'Glitchless']

        option_category = AutocompleteCombobox(frame_category, category_list)
        option_category.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return frame_category

    def make_time(self, root):
        frame_time = ttk.Frame(root)
        text = 'Start time at:'.ljust(self.label_pad)
        label_time = ttk.Label(frame_time, text=text)
        label_time.pack(side=tk.LEFT)

        entry_time = ttk.Entry(frame_time)
        entry_time.insert(tk.END, '0.00')
        entry_time.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return frame_time

    def make_attempts(self, root):
        frame_attempts = ttk.Frame(root)
        text = 'Attempts:'.ljust(self.label_pad)
        label_attempts = ttk.Label(frame_attempts, text=text)
        label_attempts.pack(side=tk.LEFT)

        entry_attempts = ttk.Entry(frame_attempts)
        entry_attempts.insert(tk.END, '1')
        entry_attempts.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return frame_attempts

    def make_tree(self, root):
        columns = ('Icon', 'Segment Name', 'Split Time',
                   'Segment Time', 'Best Segment')
        widths = (64, 320, 128, 128, 128)
        anchors = (tk.CENTER, tk.W, tk.E, tk.E, tk.E)

        tree = ttk.Treeview(root, columns=columns, height=10)
        tree.column('#0', width=0, minwidth=0)
        params = (columns, widths, anchors)
        for idx, (column, width, anchor) in enumerate(zip(*params), 1):
            tree.heading(f'#{idx}', text=column, anchor=anchor)
            tree.column(column, width=width, anchor=anchor)

        for _ in range(3):
            tree.insert(parent='', index=tk.END,
                        values=('icon', 'Frickin Boo',
                                '10:59:59', '10:59:59', '10:59:59'))
        return tree


class TextEditBox(TopLevelBase):
    """Creates a window to edit text from root."""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root
        self.default = 'Enter a new label.'

        self.entry = None
        self.button_change = None
        self.button_exit = None

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
        entry = ttk.Entry(self)
        entry.grid(row=0, column=0)
        entry.config(width=self.winfo_reqwidth())
        entry.insert(0, self.default)
        # entry.config(fg='grey')
        entry.bind('<FocusIn>', self.focus_in)
        entry.bind('<FocusOut>', self.focus_out)
        self.entry = entry

    def focus_in(self, event):
        """Empties the entry if no user input."""
        # pylint: disable=unused-argument
        if self.entry.get() == self.default:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, '')
            # self.entry.config(fg='black')

    def focus_out(self, event):
        """Inserts an edit message if no user input."""
        # pylint: disable=unused-argument
        if self.entry.get() == '':
            self.entry.insert(0, self.default)
            # self.entry.config(fg='grey')

    def make_buttons(self):
        """Makes the button widgets."""
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, sticky=tk.NSEW)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(1):
            frame.grid_rowconfigure(row, weight=1)

        button_change = ttk.Button(frame, text='Change', command=self.get_text)
        button_change.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_change = button_change

        button_exit = ttk.Button(frame, text='Exit', command=self.destroy)
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
    STYLE = ThemedStyle(APP)
    STYLE.set_theme('black')
    APP.mainloop()
