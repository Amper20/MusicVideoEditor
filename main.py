import sys
import mido
import time
import rtmidi
from mido import MidiFile
import pygame.midi

tempo = 500000  # equivalent to 120 bpm

def set_tempo(midifile):
    for track in midifile.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo

# type 0 (single track): all messages are saved in one track
def type0(midifile):
    assert isinstance(midifile, MidiFile)

# type 1 (synchronous): all tracks start at the same time
def type1(midifile):
    assert isinstance(midifile, MidiFile)
    set_tempo(midifile)

    port = mido.open_output('Microsoft GS Wavetable Synth 0')

    for msg in midifile.play():
        print(msg)
        port.send(msg)


# type 2 (asynchronous): each track is independent of the others
def type2(midifile):
    assert isinstance(midifile, MidiFile)


midifile = MidiFile('test.mid', clip=True)
print(mido.get_output_names())
playType = {0: type0, 1: type1, 2: type2}
playType[midifile.type](midifile)

