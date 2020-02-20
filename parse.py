import sys
import mido
import time
import rtmidi
from mido import MidiFile
import pygame.midi
from moviepy.editor import *

tempo = 0  # equivalent to 120 bpm

def get_tempo(midifile):
    for track in midifile.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return msg.tempo

def get_timeline(midifile):
    channel = {}  # channel : [(midi events, time)]

    for track in midifile.tracks:
        for msg in track:
            if msg.type is 'note_on' or msg.type is 'note_off':
                lst = channel.get(msg.channel, [])
                lst.append((msg, msg.time))
                channel[msg.channel] = lst

    for (key, value) in channel.items():
        for index in range(1, len(value)):
            value[index] = (value[index][0], value[index][1] + value[index - 1][1])

    for (key, value) in channel.items():
        for index in range(0, len(value)):
            value[index] = (value[index][0], mido.tick2second(value[index][1], midifile.ticks_per_beat, tempo))

    timeline = []
    for (key, value) in channel.items():
        timeline += value
    timeline.sort(key=lambda x: x[1])
    timeline.reverse()
    return timeline

def parse_msg(timeline):
    timeline.reverse()
    notes = {} # (note, ch) : [(start, end, msg)]
    for index in range(0, len(timeline)):
        msg = timeline[index][0]
        if(msg.type == 'note_on' and msg.velocity != 0):
            strt = msg
            for j in range(index + 1, len(timeline)):
                msg1 = timeline[j][0]
                if(msg.note == msg1.note and (msg1.type == 'note_off' or msg1.velocity == 0)):
                    end = msg1
                    lst = notes.get((msg.note, msg.channel), [])
                    lst.append((timeline[index][1], timeline[j][1], msg))
                    notes[(msg.note, msg.channel)] = lst
                    break
    print(notes)
# type 0 (single track): all messages are saved in one track
def type0(midifile):
    assert isinstance(midifile, MidiFile)

# type 1 (synchronous): all tracks start at the same time
def type1(midifile):

    assert isinstance(midifile, MidiFile)

    port = mido.open_output('Microsoft GS Wavetable Synth 0')
    timeline = get_timeline(midifile)
    time_start = time.time()
    while(timeline):
        now  = time.time() - time_start
        while(timeline and now >= timeline[-1][1]):
            port.send(timeline[-1][0])
            timeline.pop()


# type 2 (asynchronous): each track is independent of the others
def type2(midifile):
    assert isinstance(midifile, MidiFile)


midifile = MidiFile('blr.mid', clip=True)
tempo = get_tempo(midifile)

playType = {0: type0, 1: type1, 2: type2}
playType[midifile.type](midifile)

#parse_msg(get_timeline(midifile))
