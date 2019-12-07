import math
from wave_helper import *

CHANGING_AUDIO_VOL = 1.2
MAX_VOLUME = 32767
MIN_VOLUME = -32768
SAMPLE_RATE = 2000
NOTES_F = {"A": 440, "B": 494, "C": 523, "D": 587,
           "E": 659, "F": 698, "G": 784, "Q": 0}


def reverse_list(wave_list):
    """

    :param wave_list
    :return: a reverse list
    """
    updated_list = wave_list.reverse()
    return updated_list


def increase_speed_vocal(wave_list):
    """
    :param wave_list
    :return: a updated list that represent a faster speed
    """
    updated_list = []
    for i in range(0, len(wave_list), 2):
        updated_list.append(wave_list[i])
    return updated_list


def decrease_speed_vocal(wave_list):
    """
    the function appends between every two items, the average item
    :return: a updated list
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


def help_changing(littel_list, change):
    """
    the function receives a list of two numbers and additional number,
    and multiplies or divides the
     numbers on the list according to the number that in the 'change'
    """
    if change == 2:
        for i in range(len(littel_list)):
            littel_list[i] = int(littel_list[i] / CHANGING_AUDIO_VOL)
    elif change == 1:
        for i in range(len(littel_list)):
            littel_list[i] = int(littel_list[i] * CHANGING_AUDIO_VOL)
    return littel_list


def changing_audio(wave_list, change):
    """
    :param wave_list, change: 1= increasing 2=reducing
    :return: updated list according to the number in the "change"
             if the number is 1 the function multiplies all the
             numbers in the list by 1.2 and returns a integer
             list of lists
             if the number is 2 the function divides all the numbers
             in the list by 1.2 and returns a list with
             integer lists of numbers
             the The biggest number in the list is 32767
             the The smallest number in the list is -32768
    """
    for i in range(len(wave_list)):
        wave_list[i] = help_changing(wave_list[i], change)
    for i in range(len(wave_list)):
        for j in range(len(wave_list[i])):
            if wave_list[i][j] > MAX_VOLUME:
                wave_list[i][j] = MAX_VOLUME
            elif wave_list[i][j] < MIN_VOLUME:
                wave_list[i][j] = MIN_VOLUME
    return wave_list


def avg_function(num1, num2, num3):
    """
    :param num1, num2 , num3
    :return: the average of the numbers
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


def dimming_audio(wave_list):
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
        cycles = int(2000 * (time / 16))
        frequency = NOTES_F[note]
        if frequency == 0:  # silence
            single_note_data = [[0, 0] for _ in range(cycles)]
        else:  # real note
            samples_per_cycle = sample_rate / frequency
            for i in range(cycles):
                val_in_i = MAX_VOLUME * math.sin(
                    (2 * pi * i) / samples_per_cycle)
                int_val = int(val_in_i)
                single_note_data.append([int_val, int_val])
        return single_note_data

    result = []
    for note, time in instructions_list:
        result.extend(compose_single_note(note, int(time)))
    return result


def test1():
    wave_file = load_wave("seinfeld.wav")
    if wave_file == -1:
        print("oopsy......")

    else:
        frame_rate = wave_file[0]
        audio_data = wave_file[1]
        audio_data = dimming_audio(audio_data)
        audio_data = dimming_audio(audio_data)
        audio_data = dimming_audio(audio_data)
        audio_data = dimming_audio(audio_data)
        save_wave(frame_rate, audio_data, "notseinfeld.wav")


def main():
    main_menu_msg = "Hello, please choose one of the following options:\n" \
                    "To edit an existing wav file-  enter: '1'\n" \
                    "To compose a new wav file-     enter: '2'\n" \
                    "To exit and close the program- enter: '3'"
    choice = get_choice_from_menu(main_menu_msg, ['1', '2', '3'])
    if choice == '1':
        pass


def get_choice_from_menu(menu_msg, possible_choices):
    print(menu_msg)
    choice = input()
    while choice not in possible_choices:
        choice = input("Invalid input, please try again:")
    return choice


def test2():
    insructions_LoT = []
    with open("sample1.txt", "r") as f:
        notes_list = f.read().split()
        for i in range(0, len(notes_list) - 1, 2):
            insructions_LoT.append((notes_list[i], notes_list[i + 1]))

    audio_data = compose_from_lot(insructions_LoT)
    save_wave(SAMPLE_RATE, audio_data,
              "TETING.wav")


if __name__ == "__main__":
    main()
