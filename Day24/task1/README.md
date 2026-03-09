# Face Point Segregation using K-means

This task takes a face image, extracts facial landmarks, and groups those points using **K-means clustering**.
It then labels the clusters as regions like **left eye, right eye, nose, mouth, and face region** using centroid-based rules.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python face_kmeans_segmentation.py --input sample_face.jpg --output output.png --clusters 5 --show
```

Optional custom model path:

```bash
python face_kmeans_segmentation.py --input sample_face.jpg --output output.png --clusters 5 --model models/face_landmarker.task
```

## Notes

- Best results come from a clear, front-facing single-person image.
- Default clusters = 5 (good for rough separation into eyes/nose/mouth/other).
- On first run, the script auto-downloads `face_landmarker.task` into `models/` (internet required once).
