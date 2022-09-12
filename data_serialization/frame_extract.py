import cv2
import os

"""
extracts .jpg frames from a movie file and populates into /frame_per_second/ directory
extracts one .jpg per second of film
to use, place movie file in /input_videos/ and change title and optional scale_percent
"""

# create frames from video file
title = 'margaux'
scale_percent = 100     # no image scaling
# scale_percent = 44.44     # optional image scaling, 1080p to 480p

'''change above parameters'''

cap = cv2.VideoCapture('../input_videos/' + title + '.mkv')
# cap = cv2.VideoCapture('input_videos/' + title + '.mp4')
output_directory = os.path.join('../frame_per_second/', title)
os.mkdir(output_directory)

if not cap.isOpened():
    print("Error opening video stream or file")

frame_rate = cap.get(5)              # frame rate
print('Video frame rate:', frame_rate)  # most movie files will have a frame_rate of 23.976 frames per second


# because of the 23.976 fps frame_rate, we can't just capture every 24 frames
count = 1   # starts at 1, because first image isn't saved until 25th frame (timestamp of 1.001 seconds)
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    if cap.get(0) / 1000 >= count:     # first frame after 1 second, 2 seconds, etc.
        filename = output_directory + '/' + title + '_frame_%d.jpg' % count

        # optional image scaling
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dimensions = (width, height)
        frame = cv2.resize(frame, dimensions)

        print(cap.get(0), cap.get(1), count)
        cv2.imwrite(filename, frame)
        count += 1

cap.release()
print('Extracted', count - 1, 'frames')
