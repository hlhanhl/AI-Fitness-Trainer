import numpy as np
import math
import json
from FindRepeatingMotion import FindRepeatingMotion
import TrackMotionMediaPipe
import TrackMotionLucasKanade
import cv2
print('Collecting points with MediaPipe')
TrackMotionMediaPipe.main()
input('continue?')
print('Collecting points with Corner Detection and LK Optical Flow')
TrackMotionLucasKanade.main()
input('continue?')
