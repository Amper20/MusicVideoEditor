import sys
import mido
import time
from mido import MidiFile

filename = sys.argv[1]
import pygame.midi


pygame.midi.init()

print (pygame.midi.get_default_output_id())
print (pygame.midi.get_device_info(0))

player = pygame.midi.Output(0)

player.set_instrument(0)


midifile = MidiFile('test.mid', clip=True)
print(midifile)
for msg in midifile.play():
    if msg.type == 'note_on' or msg.type == 'note_off':
            print(msg)
            player.note_on(msg.note, 127)
            time.sleep(msg.time)

pygame.midi.quit()
