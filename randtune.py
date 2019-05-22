#!/usr/bin/python3
# Copyright (c) 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import mido
import random
import sys
import time
import argparse

parser = argparse.ArgumentParser(description='Play a random tune.')
parser.add_argument('gen_args', metavar='N', type=str, nargs='+',
                    help='argument to generator')
parser.add_argument('--root', dest='root', type = int, default=60,
                    help='root note of scale (default: 60)')
parser.add_argument('--tempo', dest='tempo', type = float, default=120,
                    help='tempo in bpm (default: 120)')
parser.add_argument('--synth', dest='synth', type = str, default=None,
                    help='synthesizer port')
parser.add_argument('--scale', dest='scale', type = str, default=None,
                    help='scale type')

args = parser.parse_args()

# MIDI random tune generator

if args.scale == "major":
    scale = [0, 2, 4, 5, 7, 9, 11]
elif args.scale == "minor":
    scale = [0, 2, 3, 5, 7, 9, 10]
elif args.scale == None:
    scale = list(range(12))
else:
    assert False

# Synthesizer port.
synth = args.synth
assert synth != None

# Beats per minute.
duration = 60.0/args.tempo

# Root note.

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

def gen_gauss(obj, note_base, note_range, note_stddev):
    obj.note_base = int(note_base)
    obj.note_range = int(note_range)
    obj.note_stddev = int(note_stddev)
    def gen(self):
        while True:
            note = int(random.gauss(self.note_range // 2, self.note_stddev)) + self.note_base
            if (note >= self.note_base) and (note <= self.note_base + self.note_range):
                return note
    return gen

generators = [
    ("silence", gen_silence),
    ("white", gen_white),
    ("gauss", gen_gauss),
]

class Tunegen(object):
    """Tune generator class"""
    def __init__(self):
        # Connect to the synth. XXX Name hardwired for now.
        self.outport = mido.open_output(synth)
        assert self.outport != None

        # Create the tune generator.
        for name, fun in generators:
            if name == args.gen_args[0]:
                self.gen = fun(self, *args.gen_args[1:])
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
