from importlib.resources import path
from pprint import pprint
from statistics import mean
import music21
from note_pair import NotePair
from type21 import *
from difficulty import *
from mido import MidiFile
import os
from csv import writer
import csv

# print name of piece
def print_name(path_name):
    mid = MidiFile(path_name, clip=True)
    pprint(mid.tracks[0])
    print("------")
    # details = []
    # details.append(mid.tracks[0][0])
    # details.append(mid.tracks[0][3])
    # details.append(mid.tracks[0][2])

    # for message in details:
    #     print(str(message).split("'")[1])
        # print(message)
    # print(mid.tracks[0][0])
    # print(mid.tracks[0][3])
    # print(mid.tracks[0][2])
    # name_message = mid.tracks[0][0]
    # mvt_message = mid.tracks[0][3]
    # artist_message = mid.tracks[0][2]


# extract the bassoon part from a score
def extract_part(score):
    bsn_names = ["bassoon", "fagotti", "basson", "fagott", "fagotto", "fagot", "fagote", "dulcian"]
    index = -1
    # find which part is the bassoon part
    for idx, part in enumerate(score):
        # print(part.partName.lower())
        for name in bsn_names:
            if name in part.partName.lower():
                index = idx
                break
        if index != -1:
            break
        # if part.partName.lower() in bsn_names:
        #     print(part.partName.lower())
        #     break
    # print(index)
    bsn_part = score.parts[index]
    return bsn_part

def extract_part_2(score):
    instrumentsSeen = 0
    for part in music21.instrument.partitionByInstrument(score):
        print(part.getInstrument().instrumentName)
        instrumentsSeen += 1
        if part.getInstrument().instrumentName == "Bassoon":
            return part
        if instrumentsSeen > 8:
            return extract_part(score)
    

def gather_info(bsn_part):
    currTempo = None
    tempoArr = []
    notesAndRestArr = []

    for n in bsn_part.recurse():
        if isChord(n):
            # notesAndRestArr.append(n)
            tempoArr.append(currTempo)
            # notesAndRestArr.append(report_note_first(n))
            sortedNotes = n.sortAscending()
            notesAndRestArr.append(sortedNotes[-1])
        elif isNote(n):
            notesAndRestArr.append(n)
            tempoArr.append(currTempo)
        elif type(n) == music21.tempo.MetronomeMark:
            currTempo = n.number
        elif isRest(n):
            notesAndRestArr.append(n)
            tempoArr.append(currTempo)

    return notesAndRestArr, tempoArr

def calculate_difficulties(notesAndRestArr, tempoArr):
    end = len(notesAndRestArr)
    total_difficulty_arr = []
    # calculate difficulties throughout the whole piece
    for i in range(0, end):
        # if the index that we're looking at is a note or a chord, add its difficulty to the total difficulty
        if isNote(notesAndRestArr[i]) or isChord(notesAndRestArr[i]):
            item = return_difficulty(i, tempoArr[i], notesAndRestArr)
            total_difficulty_arr.append(item)
    return total_difficulty_arr

def print_report(total_difficulty_arr):
    degree_of_specificity = 4
    # print floating point numbers with 2 decimal places
    print("Max of difficulties  :", round(max(total_difficulty_arr), degree_of_specificity))
    print("Mean of difficulties :", round(mean(total_difficulty_arr), degree_of_specificity))
    print("Sum of difficulties  :", round(sum(total_difficulty_arr), degree_of_specificity))

def record_report_to_csv(total_difficulty_arr, path_name, filename):
    # write path_name, mean of difficulties, max of difficulties, sum of difficulties to a csv file
    # with open(filename, 'w') as f:
    #     # write the header
    #     f.write("path_name, mean of difficulties, max of difficulties, sum of difficulties\n")
    #     # append the data
    #     f.append(path_name + "," + str(mean(total_difficulty_arr)) + "," + str(max(total_difficulty_arr)) + "," + str(sum(total_difficulty_arr)) + "\n")

    # create a list with path_name, mean of difficulties, max of difficulties, sum of difficulties
    data = [path_name, mean(total_difficulty_arr), max(total_difficulty_arr), sum(total_difficulty_arr)]

    with open('CSVFILE.csv', 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(data)  
        # Close the file object
        f_object.close()


def main(path_name):
    # path_name = "symphony_4_1.mid"
    # print_name(path_name)
    # Parse the score and define a list of bassoon names
    print("Parsing score...")
    score = music21.converter.parse(path_name)
    # Extract the bassoon part from the score
    print("Extracting bassoon part...")
    bsn_part = extract_part(score)
    # Gather the notes and rests from the bassoon part
    print("Gathering notes and rests...")
    notesAndRestArr, tempoArr = gather_info(bsn_part)
    # Calculate the difficulties of the notes and rests
    print("Calculating difficulties...")
    total_difficulty_arr = calculate_difficulties(notesAndRestArr, tempoArr)
    print_report(total_difficulty_arr)

    return total_difficulty_arr

    # record the report to a csv file
    record_report_to_csv(total_difficulty_arr, path_name, "report_1.csv")
    # print("------")
    # do the same as above with the second method
    # # print("Extracting bassoon part...")
    # bsn_part = extract_part_2(score)
    # # print("Gathering notes and rests...")
    # notesAndRestArr, tempoArr = gather_info(bsn_part)
    # # print("Calculating difficulties...")
    # total_difficulty_arr = calculate_difficulties(notesAndRestArr, tempoArr)
    # print_report(total_difficulty_arr)
    # record_report_to_csv(total_difficulty_arr, path_name, "report_2.csv")

def run_multiple():
    with open('MozartResults.csv', 'w') as csvfile:
        # create a list with path_name, mean of difficulties, max of difficulties, sum of difficulties
        fieldnames = ['Name of Piece', 'Mean of Difficulties', 'Max of Difficulties', 'Sum of Difficulties']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # assign directory
        directory = 'Mozart'
        # iterate through all the midi files in the directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print(f)
                res = main(f)
                # write the data to the csv file
                writer.writerow({'Name of Piece': f, 'Mean of Difficulties': mean(res), 'Max of Difficulties': max(res), 'Sum of Difficulties': sum(res)})
            print("-----------------------------------------------------")

if __name__ == '__main__':
    run_multiple()
    # main("../Kunstderfuge/mozart_i/bassoon_concerto_299_1.mid")
    # main("symphony_4_1.mid")
    # main("./Beethoven/Beethoven Symphony 5 Mvt 3-4.mid")
