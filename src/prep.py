from pathlib import Path
from src.gui import run

import cv2
import numpy as np

def load(path):
    path = Path(path)
    if not path.is_file(): raise FileNotFoundError(f"Image not found: {path}")

    data = np.fromfile(str(path), dtype=np.uint8)
    img  = cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None

    if img is None: raise ValueError(f"Cannot decode image: {path}")
    return img

# 그레이 + 블러
def prep(img, blur=5):
    if blur < 1 or blur % 2 == 0: raise ValueError("blur must be a positive odd number")

    gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smooth = cv2.GaussianBlur(gray, (blur, blur), 0)

    return gray, smooth