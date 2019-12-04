import math

MAX_VOLUME = 32767
SAMPLE_RATE = 2000
NOTES_F = {"A": 440, "B": 494, "C": 523, "D": 587,
           "E": 659, "F": 698, "G": 784, "Q": 0}


def compose_from_lot(instructions_list):
    """"""

    def compose_single_note(note, time):
        pi = math.pi
        single_note_data = []
        cycles = int(2000 * (time / 16))
        frequency = NOTES_F[note]
        if frequency == 0:  # silence
            single_note_data = [[0, 0] for _ in range(cycles)]
        else:  # real note
            samples_per_cycle = SAMPLE_RATE / frequency
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


print(compose_from_lot([("Q", 1), ("F", 1)]))
