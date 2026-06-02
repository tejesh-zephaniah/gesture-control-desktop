import math

class GestureClassifier:

    def classify(self, fingers, landmarks, all_hands_landmarks=None):
        # Check for two-hand peace sign → screenshot
        if all_hands_landmarks and len(all_hands_landmarks) == 2:
            if self._is_peace_sign(all_hands_landmarks):
                return "PEACE_SIGN"

        if not landmarks or not fingers:
            return None

        # Pinch gesture (thumb + index close together)
        if self._is_pinch(landmarks, fingers):
            return "CLICK"

        # Index finger only => move cursor
        if fingers == [False, True, False, False, False]:
            return "MOVE"

        # Thumb up / down only
        if fingers == [True, False, False, False, False]:
            thumb_tip_y = landmarks[4][1]
            thumb_ip_y = landmarks[3][1]

            if thumb_tip_y < thumb_ip_y - 15:
                return "THUMBS_UP"
            if thumb_tip_y > thumb_ip_y + 15:
                return "THUMBS_DOWN"
            return None

        if fingers == [True, True, True, False, False]:
            return "VOLUME_UP"
        if fingers == [True, True, True, True, False]:
            return "VOLUME_DOWN"
        if fingers == [True, False, False, False, False]:
            return "DRAG"

        return None

    def _is_pinch(self, landmarks, fingers):
        if len(landmarks) < 9:
            return False

        if fingers[:2] != [True, True]:
            return False

        thumb = landmarks[4]
        index_tip = landmarks[8]
        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        hand_size = math.hypot(middle_mcp[0] - wrist[0], middle_mcp[1] - wrist[1])
        if hand_size < 1:
            return False

        pinch_dist = math.hypot(thumb[0] - index_tip[0], thumb[1] - index_tip[1])
        return pinch_dist < hand_size * 0.16

    def _is_peace_sign(self, hands_landmarks):
        """Detect two-hand peace sign: index and middle fingers extended on both hands."""
        if len(hands_landmarks) < 2:
            return False

        # Check if both hands show peace sign (index + middle extended, ring + pinky down)
        peace_count = 0
        for hand_lms in hands_landmarks:
            if len(hand_lms) < 20:
                continue
            
            # Get finger tips and base positions
            thumb_tip = hand_lms[4]
            index_tip = hand_lms[8]
            middle_tip = hand_lms[12]
            ring_tip = hand_lms[16]
            pinky_tip = hand_lms[20]
            
            # Get wrist position for reference
            wrist = hand_lms[0]
            
            # Compute hand height
            hand_height = abs(hand_lms[9][1] - wrist[1])
            if hand_height < 1:
                continue
            
            # For peace sign:
            # - Index and middle should be extended (tips above their base)
            # - Ring and pinky should be down (tips below their base)
            index_extended = index_tip[1] < hand_lms[6][1]  # tip above PIP joint
            middle_extended = middle_tip[1] < hand_lms[10][1]  # tip above PIP joint
            ring_down = ring_tip[1] > hand_lms[14][1]  # tip below PIP joint
            pinky_down = pinky_tip[1] > hand_lms[18][1]  # tip below PIP joint
            
            # All conditions must be met
            if index_extended and middle_extended and ring_down and pinky_down:
                peace_count += 1
        
        # Both hands should show peace sign
        return peace_count >= 2