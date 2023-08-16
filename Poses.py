import cv2
import mediapipe as mp


class PoseDetector():
    def __init__(self,
                 static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                     self.enable_segmentation,
                                     self.smooth_segmentation, self.min_detection_confidence,
                                     self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.results = self.pose.process(self.imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    # def findTrack(self, img):
    #     lmList = []
    #     if self.results.pose_landmarks:
    #         for id, lm in enumerate(self.results.pose_landmarks.landmark):
    #             h, w, c = img.shape
    #             cx, cy = int(lm.x * w), int(lm.y * h)
    #             lmList.append([id, cx, cy])
    #     return  lmList
    def findPosition(self, img):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        return lmList


if __name__ == '__main__':
    pass
