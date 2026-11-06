import cv2
import numpy as np

from .prep   import prep
from .detect import find, draw
from .warp   import warp, binary
from .save   import save

def run(img, out, name, blur=5, low=50, high=100, ext="png"):
    try:
        titles = ("Original", "GrayScale", "Blur", "Edges", "Detected", "Warp", "Result", "Sliders")
        tracks = ("Blur Kernel", "Canny Low", "Canny High")

        blur = max(1, min(31, blur)) | 1
        low  = max(0, min(254, low))
        high = max(low + 1, min(255, high))

        last = flat = scan = None

        for title in titles: cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        for title, value, limit in zip(
            tracks, (blur, low, high), (31, 255, 255)
        ):  cv2.createTrackbar(title, "Sliders", value, limit, lambda _: None)
        
        print("s: 저장 | q / Esc / 창닫기: 종료")

        while True:
            raw    = tuple(cv2.getTrackbarPos(title, "Sliders") for title in tracks)
            blur   = max(1, raw[0]) | 1
            low    = min(254, raw[1])
            high   = max(low + 1, raw[2])
            values = (blur, low, high)

            if values != raw:
                for title, value in zip(tracks, values):
                    cv2.setTrackbarPos(title, "Sliders", value)
            
            if values != last:
                gray, smooth, edges = prep(img, blur, low, high)
                points = find(edges)
                result = draw(img, points)

                flat = scan = None
                if points is not None:
                    flat = warp(img, points)
                    scan = binary(flat)

                images = (img, gray, smooth, edges, result, flat, scan)

                for title, image in zip(titles, images):
                    if image is None:
                        image = np.zeros((240, 400, 3), dtype=np.uint8)
                        cv2.putText(
                            image, "No document", (30, 120),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 2
                        )
                    
                    height, width = image.shape[:2]
                    scale = min(900 / width, 700 / height, 1.0)
                    win_w = max(1, round(width  * scale))
                    win_y = max(1, round(height * scale))

                    cv2.imshow(title, image)
                    cv2.resizeWindow(title, win_w, win_y)

                last = values

            key = cv2.waitKey(30) & 0xFF

            if key in (ord("q"), 27): break

            if any(
                cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1
                for title in titles): break

            if key == ord("s"): save(flat, scan, out, name, ext)

    finally: cv2.destroyAllWindows()
