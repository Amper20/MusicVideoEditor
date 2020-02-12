import sys
import mido
import time
from mido import MidiFile

filename = sys.argv[1]
midifile = MidiFile('blr.mid')
for i, track in enumerate(midifile.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

