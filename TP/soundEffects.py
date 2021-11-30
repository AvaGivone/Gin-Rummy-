'''
    This file initializes all of the audio used in the program. 
    CITATION: 
    https://github.com/jiaaro/pydub#installation 
    Assistance for Audio also came from 112 TA's notes from S21 112 lecture on Audio

'''

from pydub import *
import simpleaudio as sa
import numpy as np

def getSound(AudioFile):
    return AudioSegment.from_file(AudioFile) # imports using pydub
   

def makesSound5Second(sound):
    return sound[:5000]

def lengthSound(sound):
    return sound.duration_seconds

def reverseSound(sound):
   return sound.reverse()

def increaseVolume(sound, dVolume):
    return sound + dVolume

def playSound(sound):
    rawAudioData = sound.raw_data # get raw data from the file
    np_array = np.frombuffer(rawAudioData, dtype=np.int16) 
    wave_obj = sa.WaveObject(np_array, 2, 2, 44100)
    return wave_obj.play()