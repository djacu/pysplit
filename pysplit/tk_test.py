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
        box.pack()


class TextEditBox(tk.Frame):
    def __init__(self, root, root2, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.root2 = root2
        self.make_widgets()

    def make_widgets(self):
        text_box = tk.Entry(self.root)
        text_box.pack()

        button_text_box = tk.Button(self.root, height=1, width=10,
                                    text='Change', command=self.get_text)
        button_text_box.pack()
        self.text_box = text_box

    def get_text(self):
        self.root2['text'] = self.text_box.get()


if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(width=200, height=400)
    app = Application(root)
    root.mainloop()
