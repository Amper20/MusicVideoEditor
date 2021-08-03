import sys
import mido
import rtmidi
import time
from mido import MidiFile
import pygame.midi
from Editor import Editor
from Player import Player

if __name__ == '__main__':

    midifile = MidiFile(r'C:\Users\Master\Desktop\MusicVideoEditor\midi_samples\blr.mid', clip=True)
    # player = Player()
    # player.play(midifile)
    editor = Editor(midifile)

