
import re
import time

from tkinter.constants import EXTENDED
import PySimpleGUI as gui

import timer as timer


def main():

    splits_window = gui.Listbox(values=['test'],
                                size=(120, 16),
                                key='splits_window',
                                select_mode=EXTENDED)
    splits_input = gui.Input(key='splits_input')
    total_timer = gui.Text('', size=(12, 2), key='total_timer')
    layout = [[splits_window], [splits_input], [total_timer],
              [gui.Text(size=(40,1), key='test_output')],
              [gui.Button('Add'),
               gui.Button('Delete'),
               gui.Button('Run', key='-RUN-PAUSE-', bind_return_key=True),
               gui.Button('Reset', key='-RESET-'),
               gui.Button('Split', key='-SPLIT-'),
               gui.Button('Quit')]]

    window = gui.Window('PySplit', layout, finalize=True)
    window.bind('<space>', '-SPLIT-')


    print('gui up and running...')

    current_time = 0
    clock = timer.Timer()

    # Display and interact with the Window using an Event Loop
    while True:
        if not clock.paused:
            event, values = window.read(timeout=1)
            current_time = clock.get_formatted()
        else:
            event, values = window.read()

        # See if user wants to quit or window was closed
        if event == gui.WINDOW_CLOSED or event == 'Quit':
            break

        # add a split
        if event == 'Add':
            update_splits(splits_window, splits_input)

        # delete a split
        if event == 'Delete':
            remove_split(splits_window)

        # reset the clock
        if event == '-RESET-':
            if clock.paused:
                current_time = 0
                clock.reset()

        if event == '-RUN-PAUSE-':
            clock.start_pause()
            current_time = clock.get_formatted()

        if event == '-SPLIT-':
            if not clock.paused:
                current_splits = splits_window.GetListValues()
                split_has_time = [i for i, x in enumerate(current_splits)
                                  if not re.search(r'\d{2}:\d{2}:\d{2}.\d{3}', x)]

                if not split_has_time:
                    pass
                else:
                    update_idx = split_has_time[0]
                    if len(current_splits) == update_idx + 1:
                        clock.pause()
                    split_to_update = current_splits[update_idx]
                    current_splits[update_idx] = (f'{split_to_update:<108}' +
                                                  clock.get_formatted())
                    splits_window.update(current_splits)


        total_timer.update(current_time)

    window.close()


def remove_split(splits_window):
    split_selection = splits_window.GetIndexes()
    current_splits = splits_window.GetListValues()
    for idx in split_selection[::-1]:
        current_splits.pop(idx)
    splits_window.update(current_splits)


def update_splits(splits_window, splits_input):
    current_splits = splits_window.GetListValues()
    current_splits.append(splits_input.Get())
    splits_window.update(current_splits)


if __name__ == '__main__':
    main()
