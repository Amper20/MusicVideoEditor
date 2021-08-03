import mido
from Event import Event

class Editor:

    def __init__(self, midi_file):
        self.tempo = self.get_tempo(midi_file)
        print(self.parse_timeline(self.get_timeline(midi_file)[0:10]))

    def parse_event(self, event):
        pass

    def get_tempo(self, midifile):
        for track in midifile.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    return msg.tempo

    def get_timeline(self, midifile):
        channel = {}  # channel : [(midi events, time)]

        for track in midifile.tracks:
            for msg in track:
                if msg.type == 'note_on' or msg.type == 'note_off':
                    lst = channel.get(msg.channel, [])
                    lst.append((msg, msg.time, msg.channel))
                    channel[msg.channel] = lst

        for (key, value) in channel.items():
            for index in range(1, len(value)):
                value[index] = (value[index][0], value[index][1] + value[index - 1][1], value[index][2])

        for (key, value) in channel.items():
            for index in range(0, len(value)):
                value[index] = Event(value[index][0], mido.tick2second(value[index][1], midifile.ticks_per_beat, self.tempo), value[index][2])

        timeline = []
        for (key, value) in channel.items():
            timeline += value
        timeline.sort(key=lambda x: x.time)

        return timeline

    def parse_timeline(self, timeline):
        notes = {}  # ch : [(msg, start, end)]
        for start in range(0, len(timeline)):
            msg_start = timeline[start].message
            if msg_start.type == 'note_on' and msg_start.velocity != 0:
                for stop in range(start + 1, len(timeline)):
                    msg_stop = timeline[stop].message
                    if (msg_start.note == msg_stop.note and
                          (msg_stop.type == 'note_off' or msg_stop.velocity == 0) and
                          msg_start.channel == msg_stop.channel):

                        notes.setdefault((msg_start.channel), []).append((timeline[start], timeline[stop]))
                        break
        return notes