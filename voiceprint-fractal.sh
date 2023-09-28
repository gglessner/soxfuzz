#!/bin/bash

./soxfuzz.py -i voiceprint.wav -o fractal.wav -l 1 -v 0.01
./soxfuzz.py -i fractal.wav -o fractal2.wav -l 0.75 -v 0.01
./soxfuzz.py -i fractal2.wav -o fractal3.wav -l 0.5 -v 0.01
./soxfuzz.py -i fractal3.wav -o fractal4.wav -l 0.25 -v 0.01
./soxfuzz.py -i fractal4.wav -o fractal5.wav -l 0.125 -v 0.01
