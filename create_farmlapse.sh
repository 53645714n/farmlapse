#!/bin/sh

#Set Path for ffmpeg Libraries
export LD_LIBRARY_PATH=/usr/lib/

ffmpeg -y -framerate 15 -pattern_type glob -i "/home/pi/pictures/*.jpg" -s:v 1440x1080 -c:v libx264 -crf 17 -pix_fmt yuv420p /home/pi/farmlapse.mp4

#EOF
