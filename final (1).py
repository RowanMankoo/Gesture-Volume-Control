from Utils import *
from HandDetector import *

import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

# volume settings
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# initalise values
min_vol, max_vol = 0,1
min_hand, max_hand = 15,110
prev_time = 0
prev_detected = False

cap = cv2.VideoCapture(0)
detector = handDetector()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    vol = volume.GetMasterVolumeLevelScalar()
    # find hands and detected landmark positions 
    detector.FindHands(frame)
    lmList = detector.LandmarkPositions(frame)
    area, bbox = BoundingBox(lmList)
    
    # checks detection of and hand whether this is first detection
    if len(lmList) == 0 or area<100:
        prev_detected = False
    else:
        if not prev_detected:
            start_time = time.time()
            prev_detected = True
        else:
            prev_detected = True
        
        # find distance from index finger to thumb
        dist = detector.Distance(frame)
        # plot bounding box of hand and hand
        cv2.rectangle(frame, bbox[0],bbox[1], (255,0,0),2)
        detector.DrawHand(frame)
        # only change volume if index finger is down
        if detector.PinkyFingerDown(frame):
            # interpolate values from hand range to volume range 
            vol = np.interp(dist,[min_hand,max_hand], [min_vol,max_vol])
            # volume increment value
            increment = 5 
            vol = increment*round(vol*100/increment)/100
            volume.SetMasterVolumeLevelScalar(vol, None)
            
        # cancel if middle finger down
        elapsed_time = time.time()-start_time
        if detector.MiddleFingerDown(frame) and elapsed_time>4:
            break
        
    
    # add volume bar display
    vol_bar = np.interp(vol, [min_vol,max_vol],[400,150])
    cv2.rectangle(frame, (50,150), (85,400), (0,255,0), 3)
    cv2.rectangle(frame, (50,int(vol_bar)), (85,400), (0,255,0), cv2.FILLED)
    
    # add volume percentage
    vol_per = np.interp(vol, [min_vol,max_vol],[0,100])
    vol_per = round(vol_per)
    cv2.putText(frame, f'{int(vol_per)} %', (40,450), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color = (0,255,0),thickness=3)
    
    
    # calculate FPS and display
    curr_time = time.time()
    fps = int(1/(curr_time-prev_time))
    prev_time = curr_time 
    cv2.putText(frame, f'FPS: {fps}', (30,50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color = (255,0,0))
    
    # print image 
    cv2.imshow('frame',frame)
    
    
    
    # cancel with 'Esc' key
    key = cv2.waitKey(1)  
    if key%256 == 27:
        break

cap.release()
cv2.destroyAllWindows()
