from pymosh import Index
from pymosh.mpeg4 import is_iframe
import sys
import os
from visvis.vvmovie import images2avi as vv
from PIL import Image

def count_frames(index):
    '''counts frames, given an indexed avi'''
    number_of_frames = 0
    for stream in index.video:
        for i in stream:
            number_of_frames += 1
    return number_of_frames

def find_image_size(old_filename):
    '''finds dimensions of given avi'''
    images = vv.readAvi(old_filename, False)
    image = images[0]
    return image.size

def write_shell(new_filename, length, duration, size):
    '''writes an avi containing only black frames of the intended final size, length, and duration'''
    frames = []
    for i in range(length):
        frames.append(Image.new("RGB",size))
    vv.writeAvi("shell.avi", frames, duration)

def process_frame(frame, buf):
    """Process a frame, holding onto one P-frame at a time, which is used to
    replace any I-frames encountered."""
    #if there is no frame in buf or the frame is not i-frame
    if buf[0] == None or not is_iframe(frame):
        #then buf is the seen p-frame 
        buf[0] = frame 
    else:
        #if it IS an iframe then use the buf'ers pframe
        frame = buf[0]
        #return the frame
    return frame
    #we use the list of frames in the loaded file

def bloom(old_filename, new_filename, wait, bloom):
    '''Creates an avi that behaves normally for (wait) frames, copies the last frame for (bloom) frames, and then continues normally until the end of the avi''' 
    f = Index(old_filename) #Allows original avi to be accessed by pymosh
    write_shell(new_filename, count_frames(f)+bloom, .05, find_image_size(old_filename)) #Creates a blank gif to be written into

    buf = [None] # So I can assign to the closed-over buffer
    
    g = Index("shell.avi") #Allows the shell avi to be written into by pymosh
    for stream in f.video: #Takes desired frames from old avi, copies them in the right order
        newstream = []
        newstream.append(stream[0])
        ix = 0
        for i in stream[1:]:
            ix+=1
            newstream.append(process_frame(stream[ix], buf))
            if ix == wait:
                for i in range(bloom):
                    newstream.append(newstream[-1])
        for gstream in g.video: #Replaces shell's black frames with old avi's frames
            gstream.replace(newstream)
    g.rebuild()
    g.write(new_filename) #Writes final gif

def shmear(old_filename, new_filename):
    '''Creates an avi with each of the P-frames doubled, hopefully creating a blurring effect'''
    f = Index(old_filename)
    write_shell(new_filename, count_frames(f)*2-1, .1, find_image_size(old_filename))

    buf = [None]

    g = Index("shell.avi")
    for stream in f.video:
        newstream = []
        newstream.append(stream[0])
        ix = 0
        for i in stream[1:]:
            ix+=1
            newstream.append(process_frame(stream[ix], buf))
            newstream.append(process_frame(stream[ix], buf))
        for gstream in g.video:
            gstream.replace(newstream)
    g.rebuild()
    g.write(new_filename)

def overlay(old_filename_1, old_filename_2, new_filename):
    '''Creates an avi where the motion of old_filename_2 is layed over old_filename_1'''
    size = find_image_size(old_filename_1)
    if size != find_image_size(old_filename_2):
        print 'Please only overlay gifs of the same dimensions'
        return None
    e = Index(old_filename_1)
    f = Index(old_filename_2)
    write_shell(new_filename, count_frames(f)+count_frames(g), .2, size)

    buf = [None]

    g = Index("shell.avi")
    newstream = []
    for stream in e.video:
        newstream.append(process_frame(stream[0]))
        ix = 0
        for i in stream[1:]:
            ix+=1
            newstream.append(process_frame(stream[ix]))
    for stream in f.video:
        ix = 0
        for i in stream:
            newstream.append(process_frame(stream[ix]))
            ix+=1
    for stream in g.video:
        stream.replace(newstream)
    g.rebuild()
    g.write(new_filename)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: {0} interval filename'.format(sys.argv[0])
        sys.exit(1)

''' try:
        wait = int(sys.argv[3])
        if wait < 2:
            raise ValueError
    except ValueError:
        print 'Interval must be an integer >= 2.'
        sys.exit(1)'''

overlay(sys.argv[1], sys.argv[2], sys.argv[3])
        
