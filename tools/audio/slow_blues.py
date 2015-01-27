from Nsound import *
import numpy as np
from numpy.random import choice, rand, random_sample

def weighted_value(values, probabilities):
    bins = np.add.accumulate(probabilities)
    return values[np.digitize(random_sample(1), bins)]

def add_note(out,instr,key_num,duration,volume):
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration,freq)
    stream *= volume
    out << stream

sr = 44100.0
Wavefile.setDefaults(sr, 16)

m = Mixer()

bass = GuitarBass(sr)

volume = 0.5

out_bass = AudioStream(sr,1)
out_wav = AudioStream(sr,1)

Wavefile.read('backing.wav',out_wav)

blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
bpm = 45 # I think it is 45
probabilities = [0.55, 0.2, 0.1, 0.1, 0.5]
durations_in_beats = [0.125, 0.25, 0.5, 1.0, 2.0]
repeat_for = [8,4,2,1,1]
durations_in_seconds = [d/(bpm/60.0) for d in durations_in_beats]
rest_prob = 0.1

add_note(out_bass, bass, blues_scale[0],durations_in_seconds[-1],volume)
in_rest = False
volume_change = 0
repeats_remaining = repeat_for[-1]-1
last_note = 0
for i in range(500):
	if repeats_remaining == 0:
		in_rest = rand() < rest_prob
		index = weighted_value(range(len(durations_in_seconds)),probabilities)
		dur = durations_in_seconds[index]
		repeats_remaining = repeat_for[index]-1
		if last_note == 0:
			interval = choice([0,1])
		elif last_note == len(blues_scale) - 1:
			interval = choice([-1,0])
		else:
			interval = choice([-1,1])
		volume_change = choice([-.02,0.0,.02])
	else:
		repeats_remaining -= 1
		if last_note == 0:
			interval = choice([0,1])
		elif last_note == len(blues_scale) - 1:
			interval = choice([-1,0])

	if in_rest:
		add_note(out_bass, bass, blues_scale[last_note],dur,0)
	else:
		volume += volume_change
		if volume > 0.75:
			volume = 0.75
		elif volume < 0.25:
			volume = 0.25
		add_note(out_bass, bass, blues_scale[last_note+interval],dur,volume)
		last_note = last_note+interval

m.add(2.25,0,out_bass)
m.add(0,0,out_wav)

m.getStream(500.0) >> "mixed.wav"