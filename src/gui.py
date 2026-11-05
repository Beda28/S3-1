import cv2

def run(img, gray, smooth, edges, result):
    for title, image in (
        ("Original" , img),
        ("Grayscale", gray),
        ("Blur"     , smooth),
        ("Edges"    , edges),
        ("Detected" , result)
    ):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()