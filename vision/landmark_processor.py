class LandmarkProcessor:

    def __init__(self):
        pass


    def extract_landmarks(self, results, frame_shape):
        """
        Convert MediaPipe landmarks into a list of (x, y) coordinates
        """
        landmark_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                for lm in hand_landmarks.landmark:
                    h, w, _ = frame_shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append((cx, cy))

        return landmark_list


    def is_finger_up(self, landmark_list, tip_id, pip_id):
        """
        Detect if a finger is UP or DOWN
        """
        if not landmark_list:
            return None

        # Check all fingers
        tip_y = landmark_list[tip_id][1]
        pip_y = landmark_list[pip_id][1]

        if tip_y < pip_y:
            return 1   # UP
        else:
            return 0   # DOWN


    def get_finger_states(self, landmark_list):
        """
        Return list like [thumb, index, middle, ring, pinky]
        """
        if not landmark_list:
            return None

        fingers = [0, 0, 0, 0, 0]

        # index, middle, ring, pinky
        fingers[0] = self.is_finger_up(landmark_list,4, 2)  
        fingers[1] = self.is_finger_up(landmark_list,8, 6)  
        fingers[2] = self.is_finger_up(landmark_list,12, 10)
        fingers[3] = self.is_finger_up(landmark_list,16, 14)
        fingers[4] = self.is_finger_up(landmark_list,20, 18)

        return fingers