import mediapipe as mp
import cv2

class HandDetector:
    def __init__(self):
        self.mp_hands= mp.solutions.hands
        self.mp_draw=mp.solutions.drawing_utils
        self.hands= self.mp_hands.Hands()
    
    def process(self, frame):
        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results= self.hands.process(rgb_frame)
        return results
    
    def draw(self,frame,results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame,hand_landmarks,self.mp_hands.HAND_CONNECTIONS) 