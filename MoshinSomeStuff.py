from pymosh import Index
from pymosh.mpeg4 import is_iframe
import sys
import os
from visvis.vvmovie import images2avi as vv
from PIL import Image

def count_frames(index):
    number_of_frames = 0
    for stream in index.video:
        for i in stream:
            number_of_frames += 1
    return number_of_frames

def find_image_size(old_filename):
    images = vv.readAvi(filename)
    image = images[0]
    return image.size

def write_shell(old_filename, new_filename, length, duration, size):
    picture = Image.new(1,size)
    for range(length):
        frames.append(picture)
    writeAvi(filename, frames, duration)


