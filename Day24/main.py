import cv2
import os

# ----------------------------
# 1. Load Image
# ----------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "face.png")

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ----------------------------
# 2. Load Haar Cascades
# ----------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# ----------------------------
# 3. Detect Face
# ----------------------------

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in faces:

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]

    # ----------------------------
    # Detect Eyes (BLUE)
    # ----------------------------
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)

    for (ex, ey, ew, eh) in eyes:
        center = (ex + ew//2, ey + eh//2)
        radius = ew//2
        cv2.circle(roi_color, center, radius, (255, 0, 0), 2)  # Blue

    # ----------------------------
    # Nose (RED) - Approximate Middle Region
    # ----------------------------
    nose_center = (w//2, h//2)
    nose_radius = w//8
    cv2.circle(roi_color, nose_center, nose_radius, (0, 0, 255), 2)

    # ----------------------------
    # Lips (BLACK) - Lower Face Region
    # ----------------------------
    lip_center = (w//2, int(h*0.75))
    lip_radius = w//6
    cv2.circle(roi_color, lip_center, lip_radius, (0, 0, 0), 2)

# ----------------------------
# 4. Show Output
# ----------------------------

cv2.imshow("Facial Feature Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()