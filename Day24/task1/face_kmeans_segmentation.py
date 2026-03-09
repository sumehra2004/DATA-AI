import argparse
from pathlib import Path
from urllib.request import urlretrieve

import cv2
import mediapipe as mp
import numpy as np
from sklearn.cluster import KMeans

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cluster facial landmark points into regions (eyes, nose, mouth, etc.) using K-means."
    )
    parser.add_argument("--input", required=True, help="Path to input image")
    parser.add_argument(
        "--output",
        default="segregated_face_points.png",
        help="Path to save output image",
    )
    parser.add_argument(
        "--clusters",
        type=int,
        default=5,
        help="Number of K-means clusters (default: 5)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display output window after processing",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Optional path to face_landmarker.task model file",
    )
    return parser.parse_args()


def get_face_landmarker_model_path(custom_model: str) -> Path:
    if custom_model:
        model_path = Path(custom_model)
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        return model_path

    model_dir = Path(__file__).parent / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "face_landmarker.task"

    if not model_path.exists():
        model_url = (
            "https://storage.googleapis.com/mediapipe-models/"
            "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
        )
        print("Downloading face landmark model...")
        urlretrieve(model_url, str(model_path))

    return model_path


def detect_landmarks(image_bgr: np.ndarray, model_path: Path) -> np.ndarray:
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

    options = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=str(model_path)),
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=1,
    )

    with vision.FaceLandmarker.create_from_options(options) as landmarker:
        results = landmarker.detect(mp_image)

    if not results.face_landmarks:
        raise ValueError("No face detected in the image. Try a clearer frontal face image.")

    h, w = image_bgr.shape[:2]
    landmarks = []
    for lm in results.face_landmarks[0]:
        x = int(lm.x * w)
        y = int(lm.y * h)
        landmarks.append([x, y])

    return np.array(landmarks, dtype=np.float32)


def semantic_labels_from_centers(centers: np.ndarray, image_shape: tuple[int, int, int]) -> dict[int, str]:
    h, w = image_shape[:2]
    image_center = np.array([w / 2, h / 2], dtype=np.float32)

    cluster_ids = list(range(len(centers)))
    label_map: dict[int, str] = {}

    # Nose: closest center to image center
    nose_id = min(cluster_ids, key=lambda i: np.linalg.norm(centers[i] - image_center))
    label_map[nose_id] = "nose"
    remaining = [i for i in cluster_ids if i != nose_id]

    if remaining:
        # Mouth: the lowest (largest y) among remaining
        mouth_id = max(remaining, key=lambda i: centers[i][1])
        label_map[mouth_id] = "mouth"
        remaining = [i for i in remaining if i != mouth_id]

    if remaining:
        # Candidate eyes are usually upper half points
        upper_half = [i for i in remaining if centers[i][1] < h * 0.6]
        eye_candidates = upper_half if len(upper_half) >= 2 else remaining

        if len(eye_candidates) >= 2:
            left_eye_id = min(eye_candidates, key=lambda i: centers[i][0])
            right_eye_id = max(eye_candidates, key=lambda i: centers[i][0])
            if left_eye_id != right_eye_id:
                label_map[left_eye_id] = "left_eye"
                label_map[right_eye_id] = "right_eye"
                remaining = [
                    i for i in remaining if i not in {left_eye_id, right_eye_id}
                ]

    for i in remaining:
        label_map[i] = "face_region"

    return label_map


def draw_clusters(
    image_bgr: np.ndarray,
    points: np.ndarray,
    labels: np.ndarray,
    centers: np.ndarray,
    semantic_names: dict[int, str],
) -> np.ndarray:
    output = image_bgr.copy()

    palette = [
        (255, 99, 71),
        (60, 179, 113),
        (30, 144, 255),
        (255, 215, 0),
        (186, 85, 211),
        (72, 209, 204),
        (255, 140, 0),
        (220, 20, 60),
    ]

    for point, cluster_id in zip(points.astype(int), labels):
        color = palette[cluster_id % len(palette)]
        cv2.circle(output, tuple(point), 1, color, -1)

    for cluster_id, center in enumerate(centers.astype(int)):
        color = palette[cluster_id % len(palette)]
        name = semantic_names.get(cluster_id, f"region_{cluster_id}")
        cv2.circle(output, tuple(center), 8, color, -1)
        cv2.putText(
            output,
            name,
            (center[0] + 8, center[1] - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA,
        )

    return output


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError("Could not read input image. Ensure it is a valid image file.")

    model_path = get_face_landmarker_model_path(args.model)
    points = detect_landmarks(image, model_path)

    if args.clusters < 2:
        raise ValueError("clusters must be at least 2")
    if args.clusters > len(points):
        raise ValueError(
            f"clusters ({args.clusters}) cannot exceed number of landmarks ({len(points)})"
        )

    kmeans = KMeans(n_clusters=args.clusters, random_state=42, n_init=10)
    cluster_ids = kmeans.fit_predict(points)
    centers = kmeans.cluster_centers_

    semantic_names = semantic_labels_from_centers(centers, image.shape)
    output = draw_clusters(image, points, cluster_ids, centers, semantic_names)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), output)

    print(f"Saved segmented output to: {output_path}")
    print("Semantic cluster labels:")
    for cid, name in sorted(semantic_names.items()):
        print(f"  cluster {cid}: {name}")

    if args.show:
        cv2.imshow("Face Landmark Segregation (K-means)", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
