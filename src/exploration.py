from posixpath import split
import music21
from music21 import corpus, instrument, tinyNotation
import pretty_midi
import mido
from mido import MidiFile
import pprint

mid = MidiFile('symphony_4_1.mid', clip=True)
# print(mid)

for track in mid.tracks:
    print(track)

for msg in mid.tracks[0]:
    print(msg)

# name_message = mid.tracks[0][0]
# mvt_message = mid.tracks[0][3]
# artist_message = mid.tracks[0][2]

# details = []
# details.append(mid.tracks[0][0])
# details.append(mid.tracks[0][3])
# details.append(mid.tracks[0][2])

# for message in details:
#     print(str(message).split("'")[1])

# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

# tinyNotation.TinyNotationStream("c4 d8 f g16 a g f#", "3/4").show()

# corpus.parseWork('symphony_4_1.mid')
# stream1 = music21.midi.translate.midiFileToStream('symphony_4_1.mid')
# instrument.partitionByInstrument(stream1)

# score = music21.converter.parse('symphony_4_1.mid')
# print(type(score)) # output: <class 'music21.stream.base.Score'>
# print(len(score.parts)) # 16 (I think part 4 is bassoon)
# score.show('text')
# ins = instrument.partitionByInstrument(score)
# print(ins)

# bassoon = score.parts[3]  # parts count from 0, 3 is bassoon
# help(bassoon)
# print(bassoon.partName.lower())
# print(type(bassoon))
# excerpt = bassoon.measures(0, 30)
# excerpt.show()

#            English plural  French German Italian Russian Spanish pre
# bsn_names = "bassoon fagotti basson fagott fagotto fagot fagote dulcian"

# for idx, part in enumerate(score):
#     # print(part.partName)
#     if part.partName.lower() in bsn_names:
#         break

# bsn_part = score.parts[idx]
# a3 = music21.note.Note('A3')
# print(a3)
# print(type(bsn_part))

# print(a3 in bsn_part)
# help(bsn_part)

# def note_record(note):
#     if note.pitch in notes_dict:
#         notes_dict[note.pitch] += 1
#     else:
#         notes_dict[note.pitch] = 1

# notes_dict = {}
# num_of_As = 0
# for el in bsn_part.recurse().notes:
#     if type(el)== music21.chord.Chord:
#         # print(el.offset, el, el.activeSite, type(el))
#         for note in el.notes:
#             note_record(note)
#         # if (a3 in el.notes):
#         #     # print(el.offset, el, el.activeSite, type(el))
#         #     num_of_As+=1
#     else:
#         note_record(el)
#             # print(el.offset, el, el.activeSite, type(el))
#             # num_of_As +=1

# # print("Number of Notes:", notes_dict)
# pprint.pprint(notes_dict)

# for el in bsn_part.flatten():
#     if a3 == el:
#         print(el.offset, el, el.activeSite)

# print(a3)
