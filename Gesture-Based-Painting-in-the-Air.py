import cv2
import mediapipe as mp
import numpy as np
import os
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# ----- Webcam setup -----
cap = cv2.VideoCapture(0)
width, height = 1280, 720
cap.set(3, width)  # Set width
cap.set(4, height)  # Set height

if not cap.isOpened():
    raise RuntimeError("!!!!!Could not access webcam. Check permissions and camera index.")

print("Webcam initialized!!!")

# ----- Canvas setup -----
imgCanvas = np.zeros((height, width, 3), np.uint8)

# ------ Load header images ------
folderPath = "/Users/prarthanaphukan/Desktop/Hand Tracking Project/Header"
if not os.path.exists(folderPath):
    raise FileNotFoundError(f"!!!!!! Folder not found: {folderPath}. Please verify the path.")

myList = os.listdir(folderPath)
myList = [f for f in myList if not f.startswith('.')]  # Filter .DS_Store
if not myList:
    raise FileNotFoundError(f"!!!!!!No header images found in {folderPath}")

print(f"Found {len(myList)} header images!!!")

overlayList = []
for im_name in sorted(myList):
    im_path = os.path.join(folderPath, im_name)
    img = cv2.imread(im_path)
    if img is not None:
        overlayList.append(img)

if not overlayList:
    raise RuntimeError("!!!!!All header images failed to load.")

header = overlayList[0]
drawColor = (0, 0, 255)  # Default to Red (BGR)
thickness = 20  # Default thickness
tipIds = [4, 8, 12, 16, 20]
xp, yp = [0, 0]

# ------- MediaPipe Hands setup -------
with mp_hands.Hands(
        min_detection_confidence=0.85,
        min_tracking_confidence=0.5,
        max_num_hands=1
) as hands:
    print("Gesture-Based-Painting-in-the-air started!!! Press 'q' to quit!!!")

    while True:
        success, image = cap.read()
        if not success:
            print("!!!! Skipping empty frame...")
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                points = [
                    [int(lm.x * width), int(lm.y * height)]
                    for lm in hand_landmarks.landmark
                ]

                if len(points) != 0:
                    x1, y1 = points[8]  # Index Finger Tip
                    x2, y2 = points[12]  # Middle Finger Tip
                    x3, y3 = points[4]  # Thumb Tip
                    # x4, y4 = points[20] # Pinky Finger Tip

                    # -------- Finger states ----------
                    fingers = []
                    # Thumb state (x-coordinate check)
                    if points[tipIds[0]][0] < points[tipIds[0] - 1][0]:
                        fingers.append(1)  # Open
                    else:
                        fingers.append(0)  # Closed

                    # 4 other fingers state (y coordinate check)
                    for id in range(1, 5):
                        fingers.append(
                            1 if points[tipIds[id]][1] < points[tipIds[id] - 2][1] else 0
                        )

                    # -------- Thickness Control Mode- Thumb (0), Index (1), and Pinky (4) UP --------
                    # Only requires Thumb, Index, and Pinky to be up. Middle (2) and Ring (3) must be DOWN.
                    is_thickness_mode = fingers[0] and fingers[1] and fingers[4] and fingers[2] == 0 and fingers[3] == 0

                    if is_thickness_mode:
                        # Calculate distance between thumb tip (4) and index tip (8)
                        dist = math.hypot(x1 - x3, y1 - y3)

                        # Map the distance to the thickness range (5 to 50)
                        min_dist, max_dist = 40, 200
                        min_thickness, max_thickness = 5, 50
                        thickness = int(np.interp(dist, [min_dist, max_dist], [min_thickness, max_thickness]))

                        # Visual feedback: Draw circles showing the chosen size
                        cv2.circle(image, (x1, y1), int(thickness / 2), (255, 255, 255), cv2.FILLED)
                        cv2.circle(image, (x3, y3), int(thickness / 2), (255, 255, 255), cv2.FILLED)
                        cv2.line(image, (x1, y1), (x3, y3), (255, 255, 255), 2)

                        # Display current thickness value
                        cv2.putText(image, f"Size: {thickness}", (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),
                                    3)

                        xp, yp = 0, 0  # Reset drawing point

                    # -------Selection Mode (Index and Middle fingers UP, others DOWN) ---------
                    # Non-selection fingers: Thumb(0), Ring(3), Pinky(4)
                    is_selection_mode = fingers[1] and fingers[2] and all(fingers[i] == 0 for i in [0, 3, 4])

                    if is_selection_mode:
                        xp, yp = 0, 0  # Reset drawing point when selecting
                        cv2.rectangle(image, (x1 - 10, y1 - 15), (x2 + 10, y2 + 23), drawColor, cv2.FILLED)

                        if (y1 < 125):  # Check if the hand is in the header region
                            # -----Color/Eraser selection logic---
                            if (300 < x1 < 400):
                                header = overlayList[0]
                                drawColor = (0, 0, 255)  # Red
                            elif (560 < x1 < 660):
                                header = overlayList[1]
                                drawColor = (255, 0, 0)  # Blue
                            elif (710 < x1 < 825):
                                header = overlayList[2]
                                drawColor = (0, 255, 0)  # Green
                            elif (980 < x1 < 1105):
                                header = overlayList[3]
                                drawColor = (0, 0, 0)  # Eraser
                        #

                    # ------ Draw Mode (Index finger UP only) ------
                    # Non-draw fingers: Thumb(0), Middle(2), Ring(3), Pinky(4)
                    is_draw_mode = fingers[1] and all(fingers[i] == 0 for i in [0, 2, 3, 4])

                    if is_draw_mode:
                        cv2.circle(image, (x1, y1), int(thickness / 2), drawColor, cv2.FILLED)

                        if xp == 0 and yp == 0:
                            xp, yp = [x1, y1]

                        if y1 > 125:  # Only draw outside the header region
                            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)

                        xp, yp = [x1, y1]
                        #

                    # ------- Clear Canvas (All fingers down (make a fist)) ------
                    if all(fingers[i] == 0 for i in range(0, 5)):
                        imgCanvas = np.zeros((height, width, 3), np.uint8)
                        xp, yp = [x1, y1]  # Prevent line from (0,0)

        # --- Combine drawings with camera image ---
        image[0:125, 0:width] = header

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 5, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

        img = cv2.bitwise_and(image, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)


        cv2.imshow('Gesture Based Painting in the Air!', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


