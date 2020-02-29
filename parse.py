import sys
import mido
import time
import rtmidi
from mido import MidiFile
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
    notes = {}  # ch : [(note, start, end, msg)]
    for start in range(0, len(timeline)):
        msg_start = timeline[start][0]
        if msg_start.type == 'note_on' and msg_start.velocity != 0:
            for stop in range(start + 1, len(timeline)):
                msg_stop = timeline[stop][0]
                if (msg_start.note == msg_stop.note and
                        (
                                msg_stop.type == 'note_off' or msg_stop.velocity == 0) and msg_start.channel == msg_stop.channel):
                    notes.setdefault((msg_stop.channel), []).append(
                        (msg_start.note, timeline[start][1], timeline[stop][1], msg_start))
                    break
    return notes

def load_clip(pitch, instrument):
    if instrument == 'guitar':
        return VideoFileClip("clips/1.mov")

# type 0 (single track): all messages are saved in one track
def type0(midifile):
    assert isinstance(midifile, MidiFile)


# type 1 (synchronous): all tracks start at the same time
def type1(midifile):
    assert isinstance(midifile, MidiFile)

    port = mido.open_output('Microsoft GS Wavetable Synth 0')
    timeline = get_timeline(midifile)
    time_start = time.time()
    while (timeline):
        now = time.time() - time_start
        while (timeline and now >= timeline[-1][1]):
            port.send(timeline[-1][0])
            timeline.pop()


# type 2 (asynchronous): each track is independent of the others
def type2(midifile):
    assert isinstance(midifile, MidiFile)


if __name__ == "__main__":
    midifile = MidiFile('midi_samples/test.mid', clip=True)
    tempo = get_tempo(midifile)

    playType = {0: type0, 1: type1, 2: type2}
    # playType[midifile.type](midifile)

    notes = parse_msg(get_timeline(midifile))
    clips = []
    for msg in (notes[1])[0:10]:
        pitch = msg[0]
        clip = load_clip(pitch, 'guitar')
        clip.set_start(msg[1])
        clip.set_duration(msg[2]-msg[1])
        clips.append(clip)
    final_clip = clips_array([clips[0:5],
                             clips[5:10]])
    final_clip.subclip(0, final_clip.duration - 0.0001).write_videofile("test1.mov")
    time.sleep(10)
    exit()
