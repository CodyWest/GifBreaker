# moshmotion.py: pymosh example by johannesgj
#
# this pymosh example uses the variable "interval" to control the amount of normal
# video frames to show before farming the reached p-frame in the same amount of 
# frames. Try it out with a low number of interval. lowest in this version is 
# interval = 2.
# it works extra well with timelapse movies! 
#
# Usage:
#   python moshmotion.py interval input-file

from pymosh import Index
from pymosh.mpeg4 import is_iframe
from visvis.vvmovie import images2avi as vv
import sys
import os

def mosh(bloom, filename, wait):
    f = Index(filename) #loads in the index of frames in the given avi file

    buf = [None] # So I can assign to the closed-over buffer
    def process_frame(frame):
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
    for stream in f.video:
        #make a new list to put in frames YOU decide
        newstream = []
        #append it with a i-frame to make it load fine in video player
        newstream.append(stream[0])
        #two variables for counting frames and interval
        ix = 0
        #stream is reduced by one since we have allready added one frame above
        for i in stream[1:]:
            ix += 1
            #if ix the counter of interval is < interval select normal frames
            if ix == wait:
                for x in range(wait):
                    newstream.append(newstream[-1])
            #else bleed the0 reached frame for interval time
            else:
               newstream.append(process_frame(stream[ix]))
        #replace original stream with same length newstream
        vv.writeAvi("long_peacock_bloom.avi", newstream, duration = .1)

    # Call rebuild to recombine the modified streams and perform any other
    # maintenance the file format needs for clean output.
    f.rebuild()

    # Finally, write the modified file .
    f.write("bloom_" + os.path.basename(filename))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: {0} interval filename'.format(sys.argv[0])
        sys.exit(1)

    try:
        interval = int(sys.argv[1])
        if interval < 2:
            raise ValueError
    except ValueError:
        print 'Interval must be an integer >= 2.'
        sys.exit(1)

    mosh(interval, sys.argv[2], int(sys.argv[3]))
