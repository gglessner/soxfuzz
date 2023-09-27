#!/usr/bin/env python3

import sox
import random
from pydub import AudioSegment
import os
import getopt, sys

# Configuration
input_filename = ""
output_filename = ""
chunk_length_ms = 0
variance = 0
chunks_path = "./chunks"  # chunks folder

def usage():
    print("\nUsage: " + sys.argv[0] + " [OPTIONS]\n")
    print("\t-i, --input\t\tInput Filename")
    print("\t-o, --output\t\tOutput Filename")
    print("\t-l, --length\t\tLength of time in seconds (0.5 = 1/2 second)")
    print("\t-v, --variance\t\tHow much to vary the chunk (0.1 = +/1 0.1)")
    print("\t-h, --help\t\tThis help message\n")
    return

try:
    opts, args  = getopt.getopt(sys.argv[1:], "hi:o:l:v:", ["help", "input=", "output=", "length=", "variance="])
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif o in ("-i", "--input"):
        input_filename = a
    elif o in ("-o", "--output"):
        output_filename = a
    elif o in ("-l", "--length"):
        chunk_length_ms = int(float(a) * 1000)
    elif o in ("-v", "--variance"):
        variance = float(a)

if not input_filename or not output_filename or chunk_length_ms == 0 or variance == 0:
    usage()
    sys.exit(2)

# Create a Transformer
tfm = sox.Transformer()

# Check file duration
input_duration = sox.file_info.duration(input_filename)
print("Input Duration: ", input_duration)

# Number of segments
num_segments = int(input_duration // (chunk_length_ms / 1000)) + 1

# Split audio file
audio = AudioSegment.from_file(input_filename)

for i in range(num_segments):
    start_time = i * chunk_length_ms
    end_time = start_time + chunk_length_ms
    segment = audio[start_time:end_time]
    segment_filename = f"{chunks_path}/chunk{i}.wav"
    new_segment_filename = f"{chunks_path}/new_chunk{i}.wav"
    segment.export(segment_filename, format="wav")
    
    # Random transformations
    #action = random.choice(["speed", "pitch", "tempo", "stretch", "vol"])
    action = random.choice(["tempo", "stretch", "vol"])
    value = random.uniform(1 - variance, 1 + variance)

    if action == "speed":
        print("["+str(i + 1)+"/"+str(num_segments)+"] Speed: ", value)
        tfm.speed(value)
    elif action == "pitch":
        print("["+str(i + 1)+"/"+str(num_segments)+"] Pitch: ", value)
        tfm.pitch(value)
    elif action == "tempo":
        print("["+str(i + 1)+"/"+str(num_segments)+"] Tempo: ", value)
        tfm.tempo(value, "s") # s = Speech
    elif action == "stretch":
        print("["+str(i + 1)+"/"+str(num_segments)+"] Stretch: ", value)
        tfm.stretch(value)
    elif action == "vol":
        print("["+str(i + 1)+"/"+str(num_segments)+"] Volume: ", value)
        tfm.vol(value, "amplitude")

    tfm.build(segment_filename, new_segment_filename)

# Join audio files
output_audio = AudioSegment.empty()

for i in range(num_segments):
    output_audio += AudioSegment.from_wav(f"{chunks_path}/new_chunk{i}.wav")
    os.remove(f"{chunks_path}/chunk{i}.wav")  # deleting the chunk
    os.remove(f"{chunks_path}/new_chunk{i}.wav")  # deleting the chunk

output_audio.export(output_filename, format="wav")
