from Utils import Euclidean_dist

import mediapipe as mp
import cv2


class handDetector:
    def __init__(
        self, min_detection_confidence=0.5, min_tracking_confidence=0.75
    ):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def FindHands(self, frame):
        # convert colour
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def DrawHand(self, frame):
        # overlay hand skeleton on frame
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS, None
                )

    def LandmarkPositions(self, frame):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[0]
            for indx, lm in enumerate(hand_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([indx, cx, cy])

        return self.lmList

    def Distance(self, frame):

        # coordinates of thumb and index finger tip respectively
        x1, y1 = self.lmList[4][1], self.lmList[4][2]
        x2, y2 = self.lmList[8][1], self.lmList[8][2]
        # plot these points
        cv2.circle(frame, (x1, y1), 14, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 14, (0, 255, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        # calculate distance
        dist = Euclidean_dist((x1, y1), (x2, y2))

        return dist

    def PinkyFingerDown(self, frame):

        x1, y1 = self.lmList[20][1], self.lmList[20][2]
        x2, y2 = self.lmList[19][1], self.lmList[19][2]
        x3, y3 = self.lmList[18][1], self.lmList[18][2]

        lowered = y1 > y2 and y1 > y3
        if lowered:
            colour = (0, 255, 0)
        else:
            colour = (0, 0, 255)

        cv2.circle(frame, (x1, y1), 4, colour, cv2.FILLED)
        cv2.circle(frame, (x2, y2), 4, colour, cv2.FILLED)
        cv2.circle(frame, (x3, y3), 4, colour, cv2.FILLED)

        return lowered

    def MiddleFingerDown(self, frame):

        x1, y1 = self.lmList[12][1], self.lmList[12][2]
        x2, y2 = self.lmList[11][1], self.lmList[11][2]
        x3, y3 = self.lmList[10][1], self.lmList[10][2]
        cv2.circle(frame, (x1, y1), 4, (0, 0, 139), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 4, (0, 0, 139), cv2.FILLED)
        cv2.circle(frame, (x3, y3), 4, (0, 0, 139), cv2.FILLED)

        lowered = y1 > y2 and y1 > y3
        return lowered
