
import re
import time

from tkinter.constants import EXTENDED
import PySimpleGUI as gui


def main():

    splits_window = gui.Listbox(values=['test'],
                                size=(120, 16),
                                key='splits_window',
                                select_mode=EXTENDED)
    splits_input = gui.Input(key='splits_input')
    total_timer = gui.Text('', size=(12, 2), key='total_timer')
    layout = [[splits_window], [splits_input], [total_timer],
              [gui.Text(size=(40,1), key='test_output')],
              [gui.Button('Ok'),
               gui.Button('Delete'),
               gui.Button('Run', key='-RUN-PAUSE-'),
               gui.Button('Reset', key='-RESET-'),
               gui.Button('Split', bind_return_key=True),
               gui.Button('Quit')]]

    window = gui.Window('PySplit', layout, finalize=True)
    # window.bind('<Key>', key)
    # window.bind('+', '-RUN-PAUSE-')
    # window.bind('<Button-3>', '-RUN-PAUSE-')


    print('gui up and running...')

    current_time = 0
    paused_time = start_time = time_in_ms()
    paused = True

    # Display and interact with the Window using an Event Loop
    while True:
        if not paused:
            event, values = window.read(timeout=1)
            current_time = time_in_ms() - start_time
        else:
            event, values = window.read()
            # current_time = 0

        # See if user wants to quit or window was closed
        if event == gui.WINDOW_CLOSED or event == 'Quit':
            break
        # add a split
        if event == 'Ok':
            update_splits(splits_window, splits_input)

        # delete a split
        if event == 'Delete':
            remove_split(splits_window)

        if event == '-RESET-':
            if paused:
                paused_time = start_time = time_in_ms()
                current_time = 0

        if event == '-RUN-PAUSE-':
            (current_time,
             start_time,
             paused_time,
             paused) = run_pause(window,
                                 current_time,
                                 start_time,
                                 paused_time,
                                 paused)

        if event == 'Split':
            if not paused:
                current_splits = splits_window.GetListValues()
                split_has_time = [i for i, x in enumerate(current_splits)
                                  if not re.search(r'\d{2}:\d{2}:\d{2}.\d{3}', x)]

                if not split_has_time:
                    pass
                else:
                    update_idx = split_has_time[0]
                    if len(current_splits) == update_idx + 1:
                        (current_time,
                         start_time,
                         paused_time,
                         paused) = run_pause(window,
                                             current_time,
                                             start_time,
                                             paused_time,
                                             paused)
                    split_to_update = current_splits[update_idx]
                    current_splits[update_idx] = (f'{split_to_update:<108}' +
                                                  get_formatted_time(current_time))
                    splits_window.update(current_splits)


        update_timer(total_timer, current_time)

    window.close()

def run_pause(window, current_time, start_time, paused_time, paused):
    paused = not paused
    if paused:
        paused_time = time_in_ms()
    else:
        start_time = start_time + time_in_ms() - paused_time
        print(current_time)
    window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
    return current_time, start_time, paused_time, paused


# def key(event):
#     print('hi')
#     print(repr(event.char), repr(event.keysym), repr(event.keycode))


def update_timer(total_timer, current_time):
    total_timer.update(get_formatted_time(current_time))

def get_formatted_time(current_time):
    remainder, milliseconds = divmod(current_time, 1000)
    remainder, seconds = divmod(remainder, 60)
    minutes, hours = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours,
                                                minutes,
                                                seconds,
                                                milliseconds)



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


def time_in_ms():
    return int(time.time() * 1000)


if __name__ == '__main__':
    main()
