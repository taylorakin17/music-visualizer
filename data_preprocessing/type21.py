import music21

def isNote(n):
    return type(n) == music21.note.Note

def isChord(n):
    return type(n) == music21.chord.Chord

def isRest(n):
    return type(n) == music21.note.Rest

# reports the note of the first bassoonist
def report_note_first(n):
    if isNote(n):
        return n
    elif isChord(n):
        sorted = n.sortAscending()
        note = sorted[-2]
        return note

# report the note of the second bassoonist
def report_note_second(n):
    if isNote(n):
        return n
    elif isChord(n):
        sorted = n.sortAscending()
        note = sorted[0]
        return note