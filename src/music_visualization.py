# imports and constants
import music21
from pprint import pprint
from difficulty import *
from note_pair import NotePair
from type21 import *
import warnings
import os
import numpy as np
import pandas as pd


# global variables
data_df = None
first_bassoon_df = None

# parse score
def parse_score(path_name):
    score = music21.converter.parse(path_name)
    return score

# extract each part from a score and organize the data into a dictionary
def extract_parts_to_data_frame(score = None, score_name = None, score_movement = None):
    global data_df
    # examine the list of parts
    partList = score.getElementsByClass(music21.stream.Part)
    pList = []
    for i in range(0, len(partList)):
        pList.append(partList[i])
        
        
    events = []

    currentNumerator = None
    currentDenominator = None
    currentInstrumentName = None
    currentPartName = None
    currTempo = None


    for eachPart in pList:
        for el in eachPart.flatten():
        # note that there are all kinds of that you get hold of when iterating through this object - some of these are below (such as pitchname, midi number etc, but by looking at the music21Object you can see all the other info is available) 
            eventDictionary = {}
            eventDictionary['offset'] = el.offset
            eventDictionary['quarterLengthDuration'] = el.duration.quarterLength
            eventDictionary['measureNumber'] = el.measureNumber
            eventDictionary['currentNumerator'] = currentNumerator
            eventDictionary['currentDenominator'] = currentDenominator
            eventDictionary['instrument'] = currentInstrumentName
            eventDictionary['part'] = currentPartName
            eventDictionary['tempo'] = currTempo
            eventDictionary['type'] = type(el)


            currentType = str(type(el))

            if currentType == "<class 'music21.meter.base.TimeSignature'>":
                currentNumerator = el.numerator
                currentDenominator = el.denominator

            if "instrument" in currentType:
                currentInstrumentName = el.instrumentName
                currentPartName = el.partName
            
            if "tempo" in currentType:
                currTempo = el.number

            if currentType == "<class 'music21.note.Rest'>":
                eventDictionary['noteObj'] = el
                eventDictionary['nameWithOctave'] = "NA"
                eventDictionary['midiNumber'] = -1
                eventDictionary['fullName'] = "Rest"
                eventDictionary['name'] = "NA"
                eventDictionary['octave'] = "NA"
                events.append(eventDictionary)


            if currentType == "<class 'music21.note.Note'>":
                eventDictionary['noteObj'] = el
                eventDictionary['nameWithOctave'] = el.nameWithOctave
                eventDictionary['midiNumber'] = el.pitches[0].midi
                eventDictionary['fullName'] = el.pitches[0].fullName
                eventDictionary['name'] = el.pitches[0].name
                eventDictionary['octave'] = el.pitches[0].octave
                events.append(eventDictionary)

            elif currentType == "<class 'music21.chord.Chord'>":
                # Record only the highest note in the chord (most likely to be first part)
                sortedNotes = el.sortAscending()
                note = sortedNotes[-1]
                eventDictionary['noteObj'] = note
                eventDictionary['nameWithOctave'] = note.nameWithOctave
                eventDictionary['midiNumber'] = note.pitches[0].midi
                eventDictionary['fullName'] = note.pitches[0].fullName
                eventDictionary['name'] = note.pitches[0].name
                eventDictionary['octave'] = note.pitches[0].octave
                events.append(eventDictionary)
           
                    
    data_df = pd.DataFrame(events)
    data_df['offsetAsFloat'] = data_df['offset'].astype(float)
    # data_df['quarterLengthDurationAsFloat'] = data_df.quarterLengthDuration.astype(float)
    data_df['scoreName'] = score_name
    data_df['movement'] = score_movement



    # currTempo = None
    # score_list = []
    # musicXML = ''

    # for part in score:
    #     try:
    #         instrument = part.getInstrument().instrumentName
    #     except:
    #         # print(part)
    #         continue
    #     for element in part.flatten():
    #         record_in_data_frame = True
    #         # define items to be added to the data frame
    #         measure = element.measureNumber
    #         note_start = None
    #         note_end = None
    #         note_obj = None
    #         pitch = None
    #         volume = None
    #         tempo = None
    #         note_type = None

    #         if isChord(element):
    #             sortedNotes = element.sortAscending()
    #             note = sortedNotes[-1]
    #             note_start = note.offset
    #             note_end = note.offset + note.quarterLength
    #             note_obj = note
    #             pitch = note.pitch.ps
    #             volume = note.volume.realized
    #             tempo = currTempo
    #             note_type = type(note)
    #             # for note in element:
    #             #     note_start = note.offset
    #             #     note_end = note.offset + note.quarterLength
    #             #     note_obj = note
    #             #     pitch = note.pitch.ps
    #             #     volume = note.volume.realized
    #             #     tempo = currTempo
    #             #     note_type = type(note)
    #         elif isNote(element):
    #             note_start = element.offset
    #             note_end = element.offset + element.quarterLength
    #             note_obj = element
    #             pitch = element.pitch.ps
    #             volume = element.volume.realized
    #             note_type = type(element)
    #         elif type(element) == music21.tempo.MetronomeMark:
    #             record_in_data_frame = False
    #             currTempo = element.number
    #         elif isRest(element):
    #             note_start = element.offset
    #             note_end = element.offset + element.quarterLength
    #             note_type = type(element)
    #         if record_in_data_frame:
    #             score_list.append([measure, note_start, note_end, note_obj, pitch, volume, currTempo, note_type, instrument])
    # return score_list

# set up data frame
def create_data_frame(score_list):
    global data_df
    data_df = pd.DataFrame(score_list, columns=['measure', 'note_start', 'note_end', 'note_obj', 'pitch', 'volume', 'tempo', 'note_type', 'instrument'])
    # data_df = data_df.sort_values(by=['note_start'])
    # data_df = data_df.reset_index(drop=True)
    return data_df

# return an altered data frame of just the first bassoon
def extract_bassoon():
    global first_bassoon_df
    df1 = data_df.loc[(data_df['instrument'] == 'Midi_71') & (data_df['note_type'] == music21.note.Note)].copy()
    # mark the duplicates of note_start column first occurence
    df1['is_duplicate'] = df1['note_start'].duplicated(keep='first')
    first_bassoon_df = df1.loc[df1['is_duplicate'] == False]

    # sort by note_obj and drop duplicates of note_start
    # first_bassoon_df = df1.sort_values('note_obj', ascending=False).drop_duplicates('note_start').sort_index()


def main():
    path = "../music/xml/scan/SonataforBassoonandPianoOp168.xml"
    score = parse_score(path)
    # df = spf.convertScoreToDF(score)
    extract_parts_to_data_frame(score, "Saint-Saens Sonata for Bassoon and Piano", "1")
    # extract_parts_to_data_frame(score, None, "1")
    # print(df.head(20))
    # with pd.option_context('display.max_rows', None,'display.max_columns', None,'display.precision', 3,):
    #     print(df)

    # create_data_frame(score_list)
    # print(data_df.head(20))
    # extract_bassoon()
    # set first_bassoon_df to a view of the data frame where the instrument is the note type is a note
    global first_bassoon_df
    first_bassoon_df = data_df[(data_df['type'] == music21.note.Note) & (data_df['measureNumber'] > 1)]
    print(first_bassoon_df.head(20))

    window_size = 9
    half_window = (window_size - 1) // 2
    rolling_diff = []
    for i in range(len(first_bassoon_df)):
        # Rolling window for the density calculation
        start = max(0, i - half_window)
        end = min(len(first_bassoon_df), i + half_window + 1)
        # get value for current row
        selected_note = first_bassoon_df['offset'].iat[i]
        # calculate the sum of 1/(distance from current row) for the notes before the current row
        values_before = first_bassoon_df['offset'][start:i].values
        values_before = 1 / (selected_note - values_before)
        # calculate the sum of 1/(distance from current row) for the notes after the current row
        values_after = first_bassoon_df['offset'][i + 1:end].values
        values_after = 1 / (values_after - selected_note)
        # get rolling window for the the notes before and after the current row
        note_before = first_bassoon_df['noteObj'].iat[i-1] if i > 0 else None
        note_after = first_bassoon_df['noteObj'].iat[i+1] if i < len(first_bassoon_df) - 1 else None
        note_current = first_bassoon_df['noteObj'].iat[i]

        # create note pairs to get the difficulties
        before_diff = NotePair(note_before, note_current).difficulty
        after_diff = NotePair(note_current, note_after).difficulty

        # multiply before and after difficulties by the rolling window sums
        before_diff_complete = sum(values_before) * before_diff
        after_diff_complete = sum(values_after) * after_diff

        # add the two sums together
        rolling_diff.append(before_diff_complete + after_diff_complete)

    # first_bassoon_df['finger_difficulty'] = rolling_diff
    first_bassoon_df.loc[:,'finger_difficulty'] = rolling_diff
    # Add the new column to the original DataFrame
    data_df.loc[first_bassoon_df.index, 'finger_difficulty'] = first_bassoon_df['finger_difficulty']

    with pd.option_context('display.max_rows', None,'display.max_columns', None,'display.precision', 3, 'display.expand_frame_repr', False):
        print(data_df)

if __name__ == '__main__':
    main()