#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import mido
import random
import sys
import time

# MIDI random tune generator

# Synthesizer port.
synth = sys.argv[1]
sys.argv = sys.argv[1:]

# Note duration.
duration = 60.0/float(sys.argv[1])
sys.argv = sys.argv[1:]

import mido
import random
import sys

def gen_silence(obj):
    def gen(self):
        return None
    return gen

def gen_white(obj, note_base, note_range):
    obj.note_base = int(note_base)
    obj.note_range = int(note_range)
    def gen(self):
        return random.randint(self.note_base, self.note_base + self.note_range)
    return gen

generators = [
    ("silence", gen_silence),
    ("white", gen_white),
]

class Tunegen(object):
    """Tune generator class"""
    def __init__(self):
        # Connect to the synth. XXX Name hardwired for now.
        self.outport = mido.open_output(synth)
        assert self.outport != None

        # Create the tune generator.
        for name, fun in generators:
            if name == sys.argv[1]:
                self.gen = fun(self, *sys.argv[2:])
                return
        assert False
    
    def play(self):
        while True:
            note = self.gen(self)
            if note == None:
                for note in range(128):
                    msg = mido.Message('note_off', note=note)
                    self.outport.send(msg)
                break
            msg = mido.Message('note_on', note=note)
            self.outport.send(msg)
            time.sleep(duration)
            msg = mido.Message('note_off', note=note)
            self.outport.send(msg)

tunegen = Tunegen()
tunegen.play()
