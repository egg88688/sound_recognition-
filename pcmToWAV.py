import wave
import numpy as np
import contextlib 
import math
from numpy import ceil, log2
from collections import deque
import librosa
import matplotlib.pyplot as plt

class pcm2wav:
    def __init__(self):
        return 
    
    def pcm2wav(self,pcm_file, wav_file, channels=1, bits=16, sample_rate=44100): #(要讀的,要寫的,...) 
        pcm = open(pcm_file, 'rb')
        # f = wave.open(pcm_file)
        pcmdata = pcm.read()
        pcm.close()

        if bits % 8 != 0:
            raise ValueError("bits % 8 must == 0. now bits:" + str(bits))

        wavfile = wave.open(wav_file, 'wb')
        wavfile.setnchannels(channels)
        wavfile.setsampwidth(bits // 8)
        wavfile.setframerate(sample_rate)
        wavfile.writeframes(pcmdata)
        wavfile.close()
    
    def duration(self,fname):
        with contextlib.closing(wave.open(fname,'r')) as f: 
            frames = f.getnframes() 
            rate = f.getframerate() 
            duration = frames/float(rate) 
            print('duration = '+ str(int(duration))) 

        return int(duration)
if __name__ == "__main__":
    pcm2 = pcm2wav()
    # pcm2.wav2pcm('./data/eeee.wav','./data/Peggy.pcm')
    pcm2.pcm2wav('./data/Peggy.pcm','./data/Peggy.wav')
    pcm2.duration('./data/Peggy.wav')