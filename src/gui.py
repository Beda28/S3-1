import cv2

def run(img):
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.imshow("Original", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()