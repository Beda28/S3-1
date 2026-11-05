import cv2

def run(img, gray, smooth, edges, result, flat, scan):
    for title, image in (
        ("Original" , img),
        ("Grayscale", gray),
        ("Blur"     , smooth),
        ("Edges"    , edges),
        ("Detected" , result),
        ("Warp"     , flat),
        ("Result"   , scan),
    ):
        if image is None: continue

        height, width = image.shape[:2]

        scale = min(900 / width, 700 / height, 1.0)
        win_w = max(1, round(width  * scale))
        win_y = max(1, round(height * scale))

        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, image)
        cv2.resizeWindow(title, win_w, win_y)

    cv2.waitKey(0)
    cv2.destroyAllWindows()