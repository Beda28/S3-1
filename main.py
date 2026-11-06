import argparse
import cv2

from pathlib    import Path
from src.prep   import load, prep
from src.gui    import run
from src.detect import find, draw
from src.warp   import warp, binary
from src.save   import save


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("image"   , type=Path)
    parser.add_argument("--no-gui", action="store_true")
    parser.add_argument("--out"   , type=Path, default=Path("outputs"))
    parser.add_argument("--blur"  , type=int , default=5)
    parser.add_argument("--low"   , type=int , default=50)
    parser.add_argument("--high"  , type=int , default=100)
    parser.add_argument("--ext"   , choices=("png", "jpg"), default="png")

    args = parser.parse_args()

    try:
        img = load(args.image)
        if not args.no_gui:
            run(img, args.out, args.image.stem,
                args.blur, args.low, args.high, args.ext)
            return 0

        gray, smooth, edges = prep(img, args.blur, args.low, args.high)

        points = find(edges)
        result = draw(img, points)

        if points is None: 
            print("문서 사각형을 찾지 못했습니다.")
            return 1
    
        flat = warp(img, points)
        scan = binary(flat)

        save(flat, scan, args.out, args.image.stem, args.ext)

        return 0 if points is not None else 1

    except (OSError, ValueError, cv2.error) as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
