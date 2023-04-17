import music21
import json

path = "../music/xml/musescore/SonataforBassoonandPianoOp168-Bassoon.musicxml"
score = music21.converter.parse(path)

musicxml_measures = []

for measure in score.recurse().getElementsByClass('Measure'):
    GEX = music21.musicxml.m21ToXml.GeneralObjectExporter(measure)
    out = GEX.parse()  # out is bytes
    outStr = out.decode('utf-8')  # now is string
    musicxml_measures.append({'measureNumber': measure.measureNumber, 'musicxml': outStr})

# save musicxml_measures to json file
with open('saint_saens_1_musicxml.json', 'w') as f:
    json.dump(musicxml_measures, f)

