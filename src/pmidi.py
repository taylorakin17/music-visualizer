import pretty_midi

# import miditoolkit
# path_midi = miditoolkit.midi.utils.example_midi_file()
# midi_obj = miditoolkit.midi.parser.MidiFile("symphony_4_1.mid")
# print(midi_obj)

# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('symphony_4_1.mid')
# Print an empirical estimate of its global tempo
print(midi_data.estimate_tempo())

# midi_data.show()