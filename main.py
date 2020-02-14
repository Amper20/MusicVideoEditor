import sys
import mido
import time
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
    for track in midifile.tracks:
        print('---------------')
        print(track)
        print('---------------')
        for msg in track:
            print(msg)


# type 2 (asynchronous): each track is independent of the others
def type2(midifile):
    assert isinstance(midifile, MidiFile)

# pygame.midi.init()
#
# print(pygame.midi.get_default_output_id())
# print(pygame.midi.get_device_info(0))
#
# player = pygame.midi.Output(0)
#
# player.set_instrument(0)

midifile = MidiFile('sng.mid', clip=True)
playType = {0: type0, 1: type1, 2: type2}
playType[midifile.type](midifile)

# pygame.midi.quit()
