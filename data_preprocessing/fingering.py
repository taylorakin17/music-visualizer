notes = {
    34: (0b10000000000000000111000001101100,), # Bb1/A#1
    35: (0b01000000000000000111000001101100,), # B1     
    36: (0b00100000000000000111000001101100,), # C2     
    37: (0b00100000000000000111010001101100,), # Db2/C#2
    38: (0b00010000000000000111000001101100,), # D2     
    39: (0b00010000000000000111100001101100,), # Eb2/D#2
    40: (0b00001000000100000111000001101100,), # E2
    41: (0b00001000000000000111000001101100,), # F2     
    42: (0b00001000000010000111000001101100, 0b00001000000000000111000001101110), # F#2/Gb2
    43: (0b00001000000000000111000001101000,), # G2     
    44: (0b00001000000000000111000001101001, 0b00001000000001000111000001101000), # Ab2/G#2
    45: (0b00001000000000000111000001100000,), # A2     
    46: (0b00001000001000000111000001100000,), # Bb2/A#2
    47: (0b00001000000000000111000001000000,), # B2     
    48: (0b00001000000000000111000000000000,), # C3     
    49: (0b00011100000000000111000000000000,), # Db3/C#3
    50: (0b00001000000000000110000000000000,), # D3     
    51: (0b00001000001000000101010000100000,), # Eb3/D#3
    52: (0b00001000000000000100000000000000,), # E3     
    53: (0b00001000000000000000000000000000,), # F3     
    54: (0b00001000000010001011000001101100, 0b00001000000000001011000001101110), # F#3/Gb3
    55: (0b00001000000000001011000001101000,), # G3     
    56: (0b00001000000000001011000001101001, 0b00001000000001001011000001101000), # Ab3/G#3
    57: (0b00000000010000000111000001100000,), # A3     
    58: (0b00000000011000000111000001100000,), # Bb3/A#3
    59: (0b00000000010000000111000001000000,), # B3     
    60: (0b00000000010000000111000000000000,), # C4     
    61: (0b00000100000000000111000000101100,), # Db4/C#4
    62: (0b00000000010000000110000000000000,), # D4     
    63: (0b00000000000000000110000000101000,), # Eb4/D#4
    64: (0b00000000000000000101100001101000,), # E4     
    65: (0b00000000000000000101100001100000,), # F4     
    66: (0b00000000000000000010100001100100,), # F#4/Gb4
    67: (0b00001000000000001011000001000100,), # G4     
    68: (0b00001000001000001011000000101000,), # Ab4/G#4
    69: (0b00000110000000000111100000001000,), # A4     
    70: (0b00000110000000000111100001100100,), # Bb4/A#4
    71: (0b00000000101000000110100001100100,), # B4     
    72: (0b00000000101000000100100001100100,), # C5     
    73: (0b00000000100000000101010001001001,), # Db5/C#5
    74: (0b00000000100000000001010000001001,), # D5     
    75: (0b00000000100000000001011000001001,), # Eb5/D#5
    76: (0b00000000100000000001011100001001,), # E5     
}


# compute number of different bits
def compute_difficulty(note1, note2):
    if note2 > 76 or note2 < 34:
        print("Received a bad note:", note2)
        print("Instead used:", note1)
        fingering_B = notes[note1]
    else: 
        fingering_B = notes[note2]
        
    fingering_A = notes[note1]
    # fingering_B = notes[note2]

    champion = 1000
    for fingering_1 in fingering_A:
        for fingering_2 in fingering_B:
            diff = compute_difference(fingering_1, fingering_2)
            if diff < champion:
                champion = diff
    
    return (champion + 1)/2
  
 

def compute_difference(finger1, finger2):
    count = 0
    # since, the numbers are less than 2^31
    # run the loop from '0' to '31' only
    for i in range(0,32):
        # right shift both the numbers by 'i' and
        # check if the bit at the 0th position is different
        if (((finger1 >>  i) & 1) != ((finger2 >>  i) & 1)):
             count=count+1
 
    return count


nn2n = {
    34:"Bb1/A#1",
    35:"B1     ",
    36:"C2     ",
    37:"Db2/C#2",
    38:"D2     ",
    39:"Eb2/D#2",
    40:"E2",
    41:"F2     ",
    42:"F#2/Gb2",
    43:"G2     ",
    44:"Ab2/G#2",
    45:"A2     ",
    46:"Bb2/A#2",
    47:"B2     ",
    48:"C3     ",
    49:"Db3/C#3",
    50:"D3     ",
    51:"Eb3/D#3",
    52:"E3     ",
    53:"F3     ",
    54:"F#3/Gb3",
    55:"G3     ",
    56:"Ab3/G#3",
    57:"A3     ",
    58:"Bb3/A#3",
    59:"B3     ",
    60:"C4     ",
    61:"Db4/C#4",
    62:"D4     ",
    63:"Eb4/D#4",
    64:"E4     ",
    65:"F4     ",
    66:"F#4/Gb4",
    67:"G4     ",
    68:"Ab4/G#4",
    69:"A4     ",
    70:"Bb4/A#4",
    71:"B4     ",
    72:"C5     ",
    73:"Db5/C#5",
    74:"D5     ",
    75:"Eb5/D#5",
    76:"E5     ",
}

# noteName = [
#     "Bb1/A#1", "B1     ", "C2     ", "Db2/C#2", "D2     ", "Eb2/D#2", "F2     ", "F#2/Gb2", "G2     ", "Ab2/G#2", "A2     ", "Bb2/A#2", "B2     ", "C3     ", "Db3/C#3", "D3     ", "Eb3/D#3", "E3     ", "F3     ", "F#3/Gb3", "G3     ", "Ab3/G#3", "A3     ", "Bb3/A#3", "B3     ", "C4     ", "Db4/C#4", "D4     ", "Eb4/D#4", "E4     ", "F4     ", "F#4/Gb4", "G4     ", "Ab4/G#4", "A4     ", "Bb4/A#4", "B4     ", "C5     ", "Db5/C#5", "D5     ", "Eb5/D#5", "E5     "
#     ]

# def test():
#     A = int(input("First Note: "))
#     B = int(input("Second Note: "))
    
#     # find number of different bits
#     print(compute_difficulty(A,  B))


def find_max():
    champ = 0
    count = 0
    for i in range(34,77):
        for j in range(34, 77):
            dif = compute_difficulty(i, j)
            print(nn2n[i], "->", nn2n[j], ":", dif)
            count += 1
            if dif > champ: champ = dif
    print("Max difficulty is", champ)
    print("Total # of Combos:", count)


#########################################################
if __name__ == '__main__':
    # find_max()
    print(compute_difficulty(53, 52))
