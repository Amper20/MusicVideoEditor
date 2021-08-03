from mido import MidiFile
import mido

class Player:

    def __init__(self):
        self.tempo = 500000

    def set_tempo(self, midifile):

        for track in midifile.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo

    # type 0 (single track): all messages are saved in one track
    def type0(self, midifile):
        assert isinstance(midifile, MidiFile)

    # type 1 (synchronous): all tracks start at the same time
    def type1(self, midifile):
        assert isinstance(midifile, MidiFile)
        self.set_tempo(midifile)

        port = mido.open_output('Microsoft GS Wavetable Synth 0')

        for msg in midifile.play():
            print(msg)
            port.send(msg)


    def type2(self, midifile):
        assert isinstance(midifile, MidiFile)

    def play(self, midifile):
        playType = {0: self.type0, 1: self.type1, 2: self.type2}
        playType[midifile.type](midifile)
