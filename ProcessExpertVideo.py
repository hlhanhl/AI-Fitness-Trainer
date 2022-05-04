import numpy as np
import math
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from FindRepeatingMotion import FindRepeatingMotion
from TrackMotionMediaPipe import extractMotionSequence
import cv2

EXPERT_VIDEO_PATH = "videos/barbellExpert.mp4"

#graph of joints and their two adjacent joints. To accommodate more workouts,
#expand to contain more joints based on landmarks.png from mediapipe.
graph = {'14':['12','16'],'13':['11','15']}

def ProcessExpertVideo():
    #segment video by frames of motion
    #extractMotionSequence(EXPERT_VIDEO_PATH,'motions/barbell_expert.npy')
    f = open('mpposes.json')
    mpdata = json.load(f)
    mp_times = FindRepeatingMotion(mpdata,5)

    #display extracted workout motion, extract angles
    print('Extracted motion:')
    cap = cv2.VideoCapture(EXPERT_VIDEO_PATH)
    fps = cap.get(5)
    print('Frames per second : ', fps,'FPS')
    frame_count = cap.get(7)
    print('Frame count : ', frame_count)
    workout = [mp_times[0],mp_times[1],mp_times[2]]
    for i in range(int(frame_count)):
        ret, img = cap.read()
        if i >= workout[0]:
            cv2.imshow('Workout',img)
            cv2.waitKey(1)
            if i == workout[2]:
                break
    cv2.destroyAllWindows()
    #img = cv2.imread('landmarks.png')
    landmarks = mpimg.imread('landmarks.png')
    plt.imshow(landmarks)
    plt.show()
    joints = input()
    joints = joints.split(',')

    #extract angles
    angles = {}
    for i in range(len(mpdata['0'])):
        if mpdata['0'][i][2]  == workout[1]:
            for j in joints:
                x,y = graph[j]
                a = np.array(mpdata[x][i][:2])
                b = np.array(mpdata[j][i][:2])
                c = np.array(mpdata[y][i][:2])
                angle = 360-math.degrees(math.acos(np.dot(a-b,c-b)/(np.linalg.norm(a-b)*np.linalg.norm(c-b))))
                angles[j]=angle


    #print('joints: ',joints)
    np.save('joints',np.array(joints))
    json_angles = json.dumps(angles)
    f = open("angles.json","w")
    f.write(json_angles)
    f.close()


ProcessExpertVideo()
