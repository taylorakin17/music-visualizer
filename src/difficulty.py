import music21
from note_pair import NotePair
from type21 import isNote, isChord, report_note_first, report_note_second

# calculate the difficulty of each note with respect to notes before it
def calculate_before_d_(currNoteIndex, tempo, nara, left_spread):
    try:
        prev_note = None
        # calculate tempo
        secondsPerBeat = 60/tempo
        # secondsPerBeat = 1
        cni = currNoteIndex - 1
        # currNote = nara[cni]
        notesSeen = 0
        accumDuration = 0
        accum_difficulty_before = 0
        while notesSeen < left_spread:
            if cni < 0:
                raise Exception("Reached beginning of array")
            currNote = nara[cni]
            # print(currNote, currNote.duration.quarterLength)
            # print(accumDuration)
            # print(accum_difficulty_before)
            # print("--")
            accumDuration += (currNote.duration.quarterLength * secondsPerBeat)
            if isNote(currNote) or isChord(currNote):
                # if this is the first note, take note of it
                if notesSeen == 0:
                    prev_note = report_note_first(currNote)
                accum_difficulty_before += 1/(accumDuration)
                notesSeen += 1
            cni -= 1
        # print(accumDifficulty)
        # print("------------")
        return accum_difficulty_before, prev_note
    except:
        if left_spread == 0:
            return 0, None
        else:
            return calculate_before_d_(currNoteIndex, tempo, nara, left_spread-1)

# calculate the difficulty of each note with respect to notes after it
def calculate_after_d_(currNoteIndex, tempo, nara, right_spread=4):
    try:
        next_note = None
        # calculate tempo
        secondsPerBeat = 60/tempo
        # secondsPerBeat = 1
        cni = currNoteIndex
        # currNote = nara[cni]
        notesSeen = 0
        accumDuration = 0
        accum_difficulty_after = 0
        while notesSeen < right_spread:
            currNote = nara[cni]
            # print(currNote, currNote.duration.quarterLength)
            # print(accumDuration)
            # print(accum_difficulty_after)
            # print("--")
            if (isNote(currNote) or isChord(currNote)) and cni != currNoteIndex:
                # if this is the first note, take note of it
                if notesSeen == 0:
                    next_note = report_note_first(currNote)
                accum_difficulty_after += 1/(accumDuration)
                notesSeen += 1
            accumDuration += (currNote.duration.quarterLength * secondsPerBeat)
            cni += 1
        # print(accum_difficulty_after)
        # print("------------")
        return accum_difficulty_after, next_note
    except:
        if right_spread == 0:
            return 0, None
        else:
            return calculate_after_d_(currNoteIndex, tempo, nara, right_spread-1)

# find index of the fifth note in the array
def find_fifth_note_index(nara):
    count_of_notes = 0
    note_index = 0
    while count_of_notes < 4:
        type_of_n = type(nara[note_index])
        note_index += 1
        if type_of_n == music21.chord.Chord or type_of_n == music21.note.Note:
            count_of_notes += 1
    return note_index

# find index of the fifth to last note in the array
def find_fifth_to_last_note_index(nara):
    count_of_notes = 0
    note_index = -1
    while count_of_notes < 4:
        type_of_n = type(nara[note_index])
        note_index -= 1
        if type_of_n == music21.chord.Chord or type_of_n == music21.note.Note:
            count_of_notes += 1

    return len(nara) + note_index

# print both parts of the difficulty for each note
def print_difficulty(currNoteIndex, tempo, nara):
    print(nara[currNoteIndex])
    accum_difficulty_before, prev_note = calculate_before_d_(currNoteIndex, tempo, nara, 4)
    accum_difficulty_after, next_note = calculate_after_d_(currNoteIndex, tempo, nara, 4)
    note_pair_before = NotePair(prev_note, report_note_first(nara[currNoteIndex]))
    note_pair_after = NotePair(report_note_first(nara[currNoteIndex]), next_note)
    before_difficulty = (accum_difficulty_before * note_pair_before.difficulty)/10
    after_difficulty = (accum_difficulty_after * note_pair_after.difficulty)/10
    print("Before Difficulty:", before_difficulty)
    print("After Difficulty:", after_difficulty)
    print("Total Difficulty:", before_difficulty + after_difficulty)
    # return total difficulty
    return before_difficulty + after_difficulty

def return_difficulty(currNoteIndex, tempo, nara):
    # print("Checkpoint 1")
    accum_difficulty_before, prev_note = calculate_before_d_(currNoteIndex, tempo, nara, 4)
    # print("Checkpoint 2")
    accum_difficulty_after, next_note = calculate_after_d_(currNoteIndex, tempo, nara, 4)
    # print("Checkpoint 3")
    note_pair_before = NotePair(prev_note, report_note_first(nara[currNoteIndex]))
    # print("Checkpoint 4")
    note_pair_after = NotePair(report_note_first(nara[currNoteIndex]), next_note)
    before_difficulty = (accum_difficulty_before * note_pair_before.difficulty)/10
    after_difficulty = (accum_difficulty_after * note_pair_after.difficulty)/10
    # print("Checkpoint 5")
    return before_difficulty + after_difficulty
