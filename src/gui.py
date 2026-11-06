import cv2

from .save import save

def run(img, gray, smooth, edges, result, flat, scan, out, name, ext):
    try:
        windows = (
            ("Original" , img),
            ("Grayscale", gray),
            ("Blur"     , smooth),
            ("Edges"    , edges),
            ("Detected" , result),
            ("Warp"     , flat),
            ("Result"   , scan),
        )
        
        for title, image in windows:
            if image is None: continue

            height, width = image.shape[:2]

            scale = min(900 / width, 700 / height, 1.0)
            win_w = max(1, round(width  * scale))
            win_y = max(1, round(height * scale))

            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.imshow(title, image)
            cv2.resizeWindow(title, win_w, win_y)
        
        print("s: 저장 | q / Esc / 창닫기: 종료")

        while True:
            key = cv2.waitKey(30) & 0xFF

            if key in (ord("q"), 27): break;
            if key ==  ord("s")     : save(flat, scan, out, name, ext)

            if any(
                cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1
                for title, image in windows
                if  image is not None): break

    finally: cv2.destroyAllWindows()