# soxfuzz
Python3 audo file fuzzer based on pysox and pydub

This is PoC code to evade biometric voiceprint checks for recorded audio.

	Usage: ./soxfuzz.py [OPTIONS]

		-i, --input		Input Filename
		-o, --output		Output Filename
		-l, --length		Length of time in seconds (0.5 = 1/2 second)
		-v, --variance		How much to vary the chunk (0.1 = +/1 0.1)
		-h, --help		This help message

Ideally the initial audio file will be processed in multiple stages.  In each stage the audio file to split into multiple parts based on the length (-l) argument and stored in the ./chunks subdirectory.  Then each chunk is randomly modified (based on the -v variance) and then recombined into the output file.

	#!/bin/bash

	./soxfuzz.py -i voiceprint.wav -o fractal.wav -l 1 -v 0.01
	./soxfuzz.py -i fractal.wav -o fractal2.wav -l 0.75 -v 0.01
	./soxfuzz.py -i fractal2.wav -o fractal3.wav -l 0.5 -v 0.01
	./soxfuzz.py -i fractal3.wav -o fractal4.wav -l 0.25 -v 0.01
	./soxfuzz.py -i fractal4.wav -o fractal5.wav -l 0.125 -v 0.01
 
Based on my observations, stage 5 audio is pretty distored.  Stage 4 seems to work.

