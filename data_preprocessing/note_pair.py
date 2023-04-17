from data_preprocessing.fingering import compute_difficulty
import data_preprocessing.type21 as type21

# NotePair takes two notes in 
class NotePair:
    def __init__(self, note1, note2):
        if type21.isNote(note1):
            self.note1 = note1.pitch.midi
        else: self.note1 = note1
        if type21.isNote(note2):
            self.note2 = note2.pitch.midi
        else: self.note2 = note2
        if note1 is None or note2 is None:
            self.difficulty = 1
        else:
            # print(self.note1, self.note2)
            self.difficulty = compute_difficulty(self.note1, self.note2)

    # def difficulty(self):
    #     return self.difficulty
    

