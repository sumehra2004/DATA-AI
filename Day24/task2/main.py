import argparse
import cv2
import numpy as np
from sklearn.cluster import DBSCAN


# -------------------------------
# HUMAN / ANIMAL CLASSIFICATION
# -------------------------------

def classify_human_or_animal(image):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        return "HUMAN", faces
    else:
        return "ANIMAL", None


# -------------------------------
# DBSCAN ON FACE REGION
# -------------------------------

def apply_dbscan_on_face(image, face_coords):
    (x, y, w, h) = face_coords
    face = image[y:y+h, x:x+w]

    h, w, _ = face.shape
    points = []

    for i in range(h):
        for j in range(w):
            points.append([j, i])

    points = np.array(points)

    clustering = DBSCAN(eps=5, min_samples=10).fit(points)
    labels = clustering.labels_

    output = face.copy()

    unique_labels = set(labels)
    colors = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (0, 255, 255),
        (255, 0, 255),
    ]

    for label in unique_labels:
        if label == -1:
            continue

        cluster_points = points[labels == label]
        color = colors[label % len(colors)]

        for pt in cluster_points:
            cv2.circle(output, tuple(pt), 1, color, -1)

    image[y:y+h, x:x+w] = output
    return image


# -------------------------------
# MAIN
# -------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    img = cv2.imread(args.input)

    if img is None:
        print("Invalid image path")
        return

    result, faces = classify_human_or_animal(img)
    print("\nDetected Type:", result)

    if result == "HUMAN":
        output = apply_dbscan_on_face(img, faces[0])
        cv2.imwrite("dbscan_output.png", output)
        print("Saved as dbscan_output.png")

        if args.show:
            cv2.imshow("DBSCAN Output", output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("Skipping clustering since image is ANIMAL.")


if __name__ == "__main__":
    main()