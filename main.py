import time

import cv2
import pyautogui
import Poses


def center(x12, y12, x24, y24, x11, y11):
    cy = (y12 + y24) // 2
    c1x = (x11 + x12) // 2
    return cy, c1x


def main():
    cap = cv2.VideoCapture(1)

    poseTracking = Poses.PoseDetector()

    ymax = 370
    ymin = 300

    left_bool = True
    right_bool = True
    esc_bool = True


    pTime = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        cTime = time.time()
        fps = int(round(1 / (cTime - pTime)))
        pTime = cTime

        poseTracking.findPose(img)
        lmList = poseTracking.findPosition(img)

        h, w, c = img.shape
        cv2.circle(img, (int(w) // 2, int(h) // 2), 10, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (240, ymax), (370, ymax), (0, 255, 0), 2)
        cv2.line(img, (240, ymin), (370, ymin), (0, 255, 0), 2)
        cv2.line(img, (0,100),(640, 100), (0, 255, 0), 2)


        if len(lmList) != 0:
            y, x = center(lmList[12][1], lmList[12][2], lmList[24][1], lmList[24][2], lmList[11][1], lmList[11][2])
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (lmList[24][1], lmList[24][2]), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (int(w) // 2, int(h) // 2), (x, y), (255, 0, 255), 3)


            if 0 <= x < 240:
                if left_bool == True:
                    pyautogui.press('a')
                    left_bool = False
            elif 240 <= x <= 370:
                if left_bool == False:
                    pyautogui.press('d')
                    left_bool = True
                elif right_bool == False:
                    pyautogui.press('a')
                    right_bool = True

            else:
                if right_bool == True:
                    pyautogui.press('d')
                    right_bool = False
            if y < ymin:
                pyautogui.press('w')
            elif y > ymax:
                pyautogui.press('s')

            if (lmList[22][2] < 100 or lmList[21][2] < 100):
                if esc_bool == True:
                    pyautogui.press('space')
                    esc_bool = False
            else:
                esc_bool = True

        cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)
        cv2.imshow('Subway Surfers', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
