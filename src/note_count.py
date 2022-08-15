from pprint import pprint
import music21

# Names for bassoon
bsn_names = "bassoon fagotti basson fagott fagotto fagot fagote dulcian"

# Parse the midi file into a music21 score
score = music21.converter.parse('symphony_4_1.mid')

# find which part is the bassoon part
for idx, part in enumerate(score):
    if part.partName.lower() in bsn_names:
        break

bsn_part = score.parts[idx]

# adds a note to a dict if not in it, increments if is in it
def note_record(note):
    if note.pitch in notes_dict:
        notes_dict[note.pitch] += 1
    else:
        notes_dict[note.pitch] = 1

# Go through score and record the number of occurrences of each note
notes_dict = {}
for el in bsn_part.recurse().notes:
    if type(el)== music21.chord.Chord:
        for note in el.notes:
            note_record(note)
    else:
        note_record(el)

pprint(notes_dict)