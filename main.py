from Utils import Euclidean_dist, BoundingBox
from HandDetector import handDetector

import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import mediapipe as mp
import cv2
import time


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.detector = handDetector()

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.min_vol, self.max_vol = 0, 1
        self.min_hand, self.max_hand = 15, 110
        self.prev_time = 0
        self.prev_detected = False

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def get_annotated_frame(self, return_frame=False):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        vol = self.volume.GetMasterVolumeLevelScalar()
        # find hands and detected landmark positions
        self.detector.FindHands(frame)
        lmList = self.detector.LandmarkPositions(frame)
        area, bbox = BoundingBox(lmList)

        # checks detection of and hand whether this is first detection
        if len(lmList) == 0 or area < 100:
            self.prev_detected = False
        else:
            if not self.prev_detected:
                start_time = time.time()
                self.prev_detected = True
            else:
                self.prev_detected = True

            # find distance from index finger to thumb
            dist = self.detector.Distance(frame)
            # plot bounding box of hand and hand
            cv2.rectangle(frame, bbox[0], bbox[1], (255, 0, 0), 2)
            self.detector.DrawHand(frame)
            # only change volume if index finger is down
            if self.detector.PinkyFingerDown(frame):
                # interpolate values from hand range to volume range
                vol = np.interp(
                    dist,
                    [self.min_hand, self.max_hand],
                    [self.min_vol, self.max_vol],
                )
                # volume increment value
                increment = 5
                vol = increment * round(vol * 100 / increment) / 100
                self.volume.SetMasterVolumeLevelScalar(vol, None)

        vol_bar = np.interp(vol, [self.min_vol, self.max_vol], [400, 150])
        cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(
            frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED
        )

        vol_per = np.interp(vol, [self.min_vol, self.max_vol], [0, 100])
        vol_per = round(vol_per)
        cv2.putText(
            frame,
            f"{int(vol_per)} %",
            (40, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
            thickness=3,
        )

        # fps calculation
        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time)
        self.prev_time = curr_time
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 255, 0),
        )
        if return_frame:
            return frame
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()

    def run(self):
        while True:
            frame = self.get_annotated_frame(return_frame=True)
            cv2.imshow("frame", frame)
            # cancel with 'Esc'/'q' key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    vc = VideoCamera()
    vc.run()
