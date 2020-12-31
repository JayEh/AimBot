# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 12:33:40 2020

@author: jarre
"""

import cv2
from collections import deque

class Webcam:
    def __init__(self):
        print('starting camera...')
        self.deque_depth = 15
        self.camera = cv2.VideoCapture(0)
        self.frame_deque = deque(maxlen=self.deque_depth)
        self.roi = None
        self.tracker = None
        self.frame_start = 0
        
        # can use these ints with self.camera.get() to learn about the camera qualities
        self.camera_props = {
            'width': 3,
            'height': 4,
            'camera_fps': 5
        }
        
        
    def process_frame(self, frame):        
        # tracker is active!! update it 
        if self.roi is not None:
            
            ok,bbox = self.tracker.update(frame)
            
            x,y,w,h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            top_left = (x, y)
            bottom_right = (x+w,y+h)
            
            if ok:
                cv2.rectangle(frame, top_left, bottom_right, (0,0,255), 2)
            
            # consider adding some status text to tell if tracker has lost target
            
        
        # compute the average time taken to perform the frame processing
        smoothed_fps = round(sum(self.frame_deque) / self.deque_depth, ndigits=2)
        cv2.putText(frame, f'FPS: {smoothed_fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)


    def capture(self):
        if (self.camera.isOpened() == False):
            print('there was an error opening the camera.')
        
        
        while self.camera.isOpened():
            # take the current time
            self.frame_start = cv2.getTickCount()
            
            # take a frame from the web cam
            (grabbed, frame) = self.camera.read()
            
            # was there some issue with the webcam?
            if (grabbed == False):
                print('grabbed was false, exiting the loop')
                break
            
            # run some processing on the frame (like tracking!)
            self.process_frame(frame)
            
            # display the frame!
            cv2.imshow('web cam', frame)
            # wait for a key stroke
            key = cv2.waitKey(1) & 0xFF
            
            # press 'q' to quit the loop
            if key == ord('q'):
                print('exit')
                break
            
            elif key == ord('s'):
                print('got the s key! pick a new ROI')
                self.tracker = cv2.TrackerKCF_create()
                self.roi = cv2.selectROI('web cam', frame)
                self.tracker.init(frame, self.roi)
                
            elif key == ord('r'):
                print('resetting the tracker! pick a new ROI')
                self.roi = None
            
            # calculate the fps and add it to a list
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - self.frame_start)
            self.frame_deque.append(fps)
                
        
        # the loop is broken, clean up and shut down
        self.camera.release()
        cv2.destroyAllWindows()


cam = Webcam()
cam.capture()


