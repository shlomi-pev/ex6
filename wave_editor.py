import math
import os
from wave_helper import *

CHANGING_AUDIO_VOL = 1.2
MAX_VOLUME = 32767
MIN_VOLUME = -32768
SAMPLE_RATE = 2000
NOTES_F = {"A": 440, "B": 494, "C": 523, "D": 587,
           "E": 659, "F": 698, "G": 784, "Q": 0}


def reverse_audio(wave_list):
    """
    the function reverses the audio data in the wae_list
    :param wave_list: a list representing audio data
    :return: the wave_list after it was reversed
    """
    wave_list.reverse()
    return wave_list


def increase_audio_speed(wave_list):
    """
    the function increases the audio speed of the wave_list
    :param wave_list: a list representing audio data
    :return: an updated audio data list corresponding to an speed increase
    """
    updated_list = []
    for i in range(0, len(wave_list), 2):
        updated_list.append(wave_list[i])
    return updated_list


def decrease_audio_speed(wave_list):
    """
    the function decreases the audio speed of the wave_list
    :param wave_list: a list representing audio data
    :return: an updated audio data list corresponding to an speed decrease
    """
    if len(wave_list) == 0:
        return []
    updated_list = [wave_list[0]]
    for i in range(len(wave_list) - 1):
        left_avg = int((wave_list[i][0] + wave_list[i + 1][0]) / 2)
        right_avg = int((wave_list[i][1] + wave_list[i + 1][1]) / 2)
        updated_list.append([left_avg, right_avg])
        updated_list.append(wave_list[i + 1])
    return updated_list


def change_single_value(little_list, indicator):
    """
    the function increases/decreases the volume if a given sample
    :param little_list: a single audio sample in the form [left_val, right_val]
    :param indicator: an indicator the indicates 1:increase 2:decrease
    :return: a single audio sample after its volume was modified.
    """
    if indicator == 2:
        for i in range(len(little_list)):
            little_list[i] = int(little_list[i] / CHANGING_AUDIO_VOL)
    elif indicator == 1:
        for i in range(len(little_list)):
            little_list[i] = int(little_list[i] * CHANGING_AUDIO_VOL)
    return little_list


def change_audio_volume(wave_list, indicator):
    """
    :param wave_list, indicator: 1= increasing 2= decreasing
    :return: updated list according to the value in the "indicator"
             if the value is 1 the function multiplies all the
             numbers in the list by 1.2 and returns a integer
             list of lists
             if the value is 2 the function divides all the numbers
             in the list by 1.2 and returns a list with
             integer lists of numbers
             the The biggest number in the list is 32767
             the The smallest number in the list is -32768
    """
    for i in range(len(wave_list)):
        wave_list[i] = change_single_value(wave_list[i], indicator)
    for i in range(len(wave_list)):
        for j in range(len(wave_list[i])):
            if wave_list[i][j] > MAX_VOLUME:
                wave_list[i][j] = MAX_VOLUME
            elif wave_list[i][j] < MIN_VOLUME:
                wave_list[i][j] = MIN_VOLUME
    return wave_list


def avg_function(num1, num2, num3):
    """
    the function calculates the average of num1, num2, num3.
    :param num1:
    :param num2:
    :param num3:
    :return: the numerical average of the numbers
    """
    return int((num1 + num2 + num3) / 3)


def append_avg(update_list, left_list, right_list):
    """
    :param update_list, left_list, right_list
    :return: the update_list with the average
    of the numbers in the lists
    """
    avg_left = int((left_list[0] + right_list[0]) / 2)
    avg_right = int((left_list[1] + right_list[1]) / 2)
    update_list.append([avg_left, avg_right])
    return update_list


def low_pass_filter(wave_list):
    """
     the function returns a new list that contains
     the average of every 3 numbers in the list
     the first couple is the average of the two first couple in the list
     and the last couple is the average of the two last couples in the list
    """
    updated_list = []
    if len(wave_list) == 0:
        return []
    #  next line deals with the first item in the Updated list
    updated_list = append_avg(updated_list, wave_list[0], wave_list[1])
    if len(wave_list) != 2:
        #  the following loop changes the values of all items in the middle
        for i in range(1, len(wave_list) - 1):
            avg_left = avg_function(wave_list[i - 1][0],
                                    wave_list[i][0], wave_list[i + 1][0])
            avg_right = avg_function(wave_list[i - 1][1],
                                     wave_list[i][1], wave_list[i + 1][1])
            updated_list.append([avg_left, avg_right])
        # next line changes the value of the last items on the list
        updated_list = append_avg(updated_list,
                                  wave_list[len(wave_list) - 2],
                                  wave_list[len(wave_list) - 1])
    return updated_list


def compose_from_lot(instructions_list, sample_rate):
    """
    this function composes a beautiful melody
    :param sample_rate: the sample rate in which the wave file
    should be composed
    :param instructions_list: list tuples in the form (NOTE, TIME)
    Where NOTE is one of the seven musical notes and TIME is in 1/16 sec
    :return: returns a list of audio data composed by the instruction list
    """

    def compose_single_note(note, time):
        pi = math.pi
        single_note_data = []
        cycles = int(sample_rate * (time / 16))
        frequency = NOTES_F[note]
        if frequency == 0:  # silence
            single_note_data = [[0, 0] for _ in range(cycles)]
        else:  # real note
            samples_per_cycle = sample_rate / frequency
            for i in range(cycles):
                val_in_i = MAX_VOLUME * math.sin((2 * pi * i) /
                                                 samples_per_cycle)
                int_val = int(val_in_i)
                single_note_data.append([int_val, int_val])
        return single_note_data

    result = []
    for note, time in instructions_list:
        result.extend(compose_single_note(note, int(time)))
    return result


def edit_wave_menu(frame_rate, audio_data):
    """
    this function lets the user edit the wave file.
    when the user is done it saves the file
    :param frame_rate: the frame rate of the samples
    :param audio_data: list of audio samples s
    :return: None
    """
    edit_menu_message = """Hello, please choose one of the following options
                        "To reverse audio-         enter: '1'
                        "To increase audio speed-  enter: '2'
                        "To decrease audio speed-  enter: '3'
                        "To increase audio volume- enter: '4'
                        "To reduce audio volume-   enter: '5'
                        "To apply low pass filter- enter: '6'
                        "To save and exit-         enter: '7
                        """
    choice = get_choice_from_menu(edit_menu_message, ['1', '2', '3', '4',
                                                      '5', '6', '7'])
    while choice != '7':
        if choice == '1':
            audio_data = reverse_audio(audio_data)
            print("the audio was reversed")
        elif choice == '2':
            audio_data = increase_audio_speed(audio_data)
            print("audio speed increased")
        elif choice == '3':
            audio_data = decrease_audio_speed(audio_data)
            print("audio speed decreased")
        elif choice == '4':
            audio_data = change_audio_volume(audio_data, 1)
            print("audio volume increased")
        elif choice == '5':
            audio_data = change_audio_volume(audio_data, 2)
            print("audio volume decreased")
        elif choice == '6':
            audio_data = low_pass_filter(audio_data)
        choice = get_choice_from_menu(edit_menu_message, ['1', '2', '3', '4',
                                                          '5', '6', '7'])
    # user entered 7, we will save the modified file
    wave_filename = input("Enter a name for the modified wav file")
    success_indicator = save_wave(frame_rate, audio_data, wave_filename)
    while success_indicator != 0:  # save failed
        wave_filename = input("There was a problem in the name, please try "
                              "again")
        success_indicator = save_wave(frame_rate, audio_data, wave_filename)


def load_wave_file():
    """
    this function loads a wave file from a name given by the users input
    :return: [frame_rate, audio_data]
    """
    wave_file_name = input("Enter the name of the wav file")
    wave_file = load_wave(wave_file_name)
    while wave_file == -1:
        wave_file_name = input("Incorrect wav file please try again")
        wave_file = load_wave(wave_file_name)
    return wave_file


def load_compose_instructions():
    """
    this function loads a compose file from a file name given by the user
    as input and returns it in a usable form.
    :return: list of tuples: (note, time)
    """
    instructions_file_name = input("Enter the instructions file name:")
    while not os.path.isfile(instructions_file_name):
        instructions_file_name = input("File not found, try again")
    instructions_list = []
    with open(instructions_file_name, "r") as f:
        notes_list = f.read().split()
        for i in range(0, len(notes_list) - 1, 2):
            instructions_list.append((notes_list[i], notes_list[i + 1]))
    return instructions_list


def main_menu():
    """
    this function displays the main menu and lets the user edit and compose
    wave files.
    :return: None
    """
    main_menu_msg = """Hello, please choose one of the following options:
                    To edit an existing wav file-  enter: '1'
                    To compose a new wav file-     enter: '2'
                    To exit and close the program- enter: '3'
                    """
    choice = get_choice_from_menu(main_menu_msg, ['1', '2', '3'])
    while True:
        if choice == '1':  # edit wave file
            wav_file = load_wave_file()
            frame_rate = wav_file[0]
            audio_data = wav_file[1]
            edit_wave_menu(frame_rate, audio_data)
        elif choice == '2':  # compose new wave file
            instructions_list = load_compose_instructions()
            audio_data = compose_from_lot(instructions_list, SAMPLE_RATE)
            edit_wave_menu(SAMPLE_RATE, audio_data)
        else:
            return
        choice = get_choice_from_menu(main_menu_msg, ['1', '2', '3'])


def get_choice_from_menu(menu_msg, possible_choices):
    """
    this function displays a menu and asks the user to choose an option
    from the menu
    :param menu_msg: the message explaining the possible choices
    :param possible_choices: a list of valid choices
    :return: a valid option chosen by the user.
    """
    print(menu_msg)
    choice = input()
    while choice not in possible_choices:
        choice = input("Invalid input, please try again:")
    return choice


if __name__ == "__main__":
    main_menu()
