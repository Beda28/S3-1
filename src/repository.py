from pathlib import Path

import cv2
import numpy as np

def load(path):
    path = Path(path)
    if not path.is_file(): raise FileNotFoundError(f"Image not found: {path}")

    data = np.fromfile(str(path), dtype=np.uint8)
    img  = cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None

    if img is None: raise ValueError(f"Cannot decode image: {path}")
    return img