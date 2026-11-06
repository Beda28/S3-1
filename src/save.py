from datetime import datetime
from pathlib  import Path

import cv2

def save(flat, scan, out, name, ext="png"):
    if flat is None or scan is None: return print("문서 검출 결과가 없어 저장하지 않았습니다.")
    if ext not in ("png", "jpg")   : raise ValueError("Use png or jpg")

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    for label, image in (("warp", flat), ("scan", scan)):
        path = out / f"{name}_{stamp}_{label}.{ext}"

        ok, data = cv2.imencode(f".{ext}", image)
        if not ok: raise OSError(f"Cannot encode image: {path}")

        data.tofile(str(path))
        print(f"Saved: {path}")